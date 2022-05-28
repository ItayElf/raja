import json
import os.path

from raja.file_handler import load_files, add_file, add_folder, generate_files_string, remove_file, remove_folder
from raja.utils import error, success


def add(path: str) -> None:
    """Adds a file or a folder to the tracked files list"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    content = load_files(open(os.path.join(".raja", ".raja_files")).read(), settings["ignored_extensions"],
                         settings["ignored_directories"], settings["ignored_files"])
    path = os.path.relpath(path, ".")
    if os.path.isfile(path):
        content = add_file(content, path, settings["ignored_extensions"], settings["ignored_files"])
    elif os.path.isdir(path):
        content = add_folder(content, path, settings["ignored_extensions"], settings["ignored_directories"],
                             settings["ignored_files"])
    else:
        error(f"invalid path: '{path}'")
        return
    with open(os.path.join(".raja", ".raja_files"), "w") as f:
        f.write(generate_files_string(content))
    success(f"{path} was added successfully.")


def remove(path: str) -> None:
    """Removes a file or a folder from the tracked files list"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    content = load_files(open(os.path.join(".raja", ".raja_files")).read(), settings["ignored_extensions"],
                         settings["ignored_directories"], settings["ignored_files"])
    path = os.path.relpath(path, ".")
    if os.path.isfile(path):
        content = remove_file(content, path, settings["ignored_extensions"], settings["ignored_files"])
    elif os.path.isdir(path):
        content = remove_folder(content, path, settings["ignored_directories"])
    else:
        error(f"invalid path: '{path}'")
        return
    with open(os.path.join(".raja", ".raja_files"), "w") as f:
        f.write(generate_files_string(content))
    success(f"{path} was removed successfully.")
