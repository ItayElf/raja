import json
import os.path

from raja.file_handler import load_files, add_file, add_folder, generate_files_string
from raja.utils import error, success


def add(path: str) -> None:
    """Adds a file or a folder to the tracked files list"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    content = load_files(open(os.path.join(".raja", ".raja_files")).read())
    path = os.path.relpath(path, ".")
    if os.path.isfile(path):
        content = add_file(content, path, settings["ignored_extensions"], settings["ignored_files"])
    elif os.path.isdir(path):
        content = add_folder(content, path, settings["ignored_extensions"], settings["ignored_directories"],
                             settings["ignored_files"])
    else:
        error(f"invalid path: {path}")
        return
    with open(os.path.join(".raja", ".raja_files"), "w") as f:
        f.write(generate_files_string(content))
    success(f"{os.path.abspath(path)} was added successfully.")
