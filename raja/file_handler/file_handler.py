from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


@dataclass
class File:
    name: str


@dataclass
class Folder:
    name: str
    files: List[File]
    sub_dirs: List[Folder]

    def __post_init__(self):
        self.name = self.name.split(os.path.sep)[-1]


def _is_file_valid(filename: str, ignored_extensions: List[str], ignored_files: List[str]) -> bool:
    """Returns true if file is valid"""
    filename = os.path.relpath(filename, "")
    return os.path.splitext(filename)[1] not in ignored_extensions and filename not in ignored_files


def _is_dir_valid(directory: str, ignored_directories: List[str]) -> bool:
    """Returns True if directory is valid"""
    return os.path.basename(os.path.normpath(directory)) not in ignored_directories


def get_all_files(directory: str = ".", ignored_extensions: List[str] = None,
                  ignored_directories: List[str] = None, ignored_files: List[str] = None) -> Folder:
    """Returns all files recursively"""
    if not ignored_extensions:
        ignored_extensions = []
    if not ignored_directories:
        ignored_directories = []
    if not ignored_files:
        ignored_files = []
    current_folder, sub_dirs, files = next(os.walk(directory))
    files = [File(os.path.relpath(os.path.join(current_folder, file), directory)) for file in files if
             _is_file_valid(os.path.join(directory, file), ignored_extensions, ignored_files)]
    files.sort(key=lambda x: x.name)
    folders = [get_all_files(os.path.join(directory, sub_dir), ignored_extensions, ignored_directories, ignored_files)
               for sub_dir in
               sub_dirs if
               _is_dir_valid(sub_dir, ignored_directories)]
    folders.sort(key=lambda x: x.name)
    return Folder(directory, files, folders)


def generate_files_string(content: Folder, root: str = "") -> str:
    """Returns formatted string that represents all the tracked files"""
    base = "\n".join([os.path.relpath(os.path.join(root, f.name), "") for f in
                      content.files]) + "\n\n"
    for d in content.sub_dirs:
        base += generate_files_string(d, os.path.join(root, d.name))
        if not base.endswith("\n"):
            base += "\n\n"
    return base.strip()


def load_files(content: str) -> Folder:
    """Returns folder object from the content of .raj_files as the root folder"""
    lines = [line for line in content.splitlines() if line]
    folder = _load_files(lines)
    folder.name = "."
    return folder


def _load_files(lines: List[str]) -> Folder:
    """Create Folder object from files file"""
    local_files = [File(line) for line in lines if os.path.sep not in line]
    nested_files = [line for line in lines if os.path.sep in line]
    sub_dirs = {line.split(os.path.sep)[0]: [] for line in nested_files}
    for file in nested_files:
        sub_dir = file.split(os.path.sep)[0]
        sub_dirs[sub_dir].append(os.path.relpath(file, sub_dir))
    directories = []
    for sub_dir, lines in sub_dirs.items():
        folder = _load_files(lines)
        folder.name = sub_dir
        directories.append(folder)
    return Folder("", local_files, directories)


def add_file(content: Folder, path_to_file: str, ignored_extensions: List[str], ignored_files: List[str]) -> Folder:
    """Adds a file to folder object"""
    if not _is_file_valid(path_to_file, ignored_extensions, ignored_files):
        return content
    folder = content
    while len(path_to_file.split(os.path.sep)) > 1:
        try:
            folder = next(filter(lambda x: x.name == path_to_file.split(os.path.sep)[0], folder.sub_dirs))
        except StopIteration:
            f = Folder(str(path_to_file.split(os.path.sep)[0]), [], [])
            folder.sub_dirs.append(f)
            folder = f
        path_to_file = os.path.join(*path_to_file.split(os.path.sep)[1:])
    if path_to_file not in [f.name for f in folder.files]:
        folder.files.append(File(path_to_file))
    return content


def add_folder(content: Folder, path_to_folder: str, ignored_extensions: List[str],
               ignored_directories: List[str], ignored_files: List[str]) -> Folder:
    """Adds a subdirectory to a folder object"""
    if not _is_dir_valid(path_to_folder, ignored_directories):
        return content
    folder = content
    path = path_to_folder
    while os.path.sep in path and path.split(os.path.sep)[0] in [d.name for d in folder.sub_dirs]:
        folder = next(filter(lambda x: x.name == path.split(os.path.sep)[0], folder.sub_dirs))
        path = os.path.join(*path.split(os.path.sep)[1:])
    if not path or path in [d.name for d in folder.sub_dirs]:
        return content
    for sub_dir in path.split(os.path.sep)[:-1]:
        f = Folder(str(sub_dir), [], [])
        folder.sub_dirs.append(f)
        folder = f
    if folder.name == path:
        f = get_all_files(path_to_folder, ignored_extensions, ignored_directories, ignored_files)
        folder.files = f.files
        folder.sub_dirs = f.sub_dirs
    else:
        folder.sub_dirs.append(get_all_files(path_to_folder, ignored_extensions, ignored_directories, ignored_files))
    return content


def remove_file(content: Folder, path_to_file: str, ignored_extensions: List[str], ignored_files: List[str]) -> Folder:
    """Removes a file from a folder object"""
    if not _is_file_valid(path_to_file, ignored_extensions, ignored_files):
        return content
    folder = content
    while len(path_to_file.split(os.path.sep)) > 1:
        try:
            folder = next(filter(lambda x: x.name == path_to_file.split(os.path.sep)[0], folder.sub_dirs))
        except StopIteration:
            raise FileNotFoundError(path_to_file)
        path_to_file = os.path.join(*path_to_file.split(os.path.sep)[1:])
    folder.files.remove(File(path_to_file))
    return content


def remove_folder(content: Folder, path_to_folder: str, ignored_directories: List[str]) -> Folder:
    """Removes a subdir from a folder object"""
    if not _is_dir_valid(path_to_folder, ignored_directories):
        return content
    folder = content
    if path_to_folder == folder.name:
        return Folder(folder.name, [], [])
    if path_to_folder.endswith(os.path.sep):
        path_to_folder = path_to_folder[:-len(os.path.sep)]
    path = path_to_folder
    while os.path.sep in path and path.split(os.path.sep)[0] in [d.name for d in folder.sub_dirs]:
        try:
            folder = next(filter(lambda x: x.name == path.split(os.path.sep)[0], folder.sub_dirs))
            path = os.path.join(*path.split(os.path.sep)[1:])
        except StopIteration:
            raise FileNotFoundError(path_to_folder)
    try:
        folder.sub_dirs.remove(next(filter(lambda x: x.name == path.split(os.path.sep)[0], folder.sub_dirs)))
    except StopIteration:
        raise FileNotFoundError(path_to_folder)
    return content
