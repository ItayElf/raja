import json
import os
import shutil

_base_settings = {
    "ignored_extensions": [],
    "ignored_directories": [],
    "ignored_files": [],
    "last_commit": None,
    "username": "",
}


def init(directory: str = ".") -> None:
    """Initialize raja workspace at the given directory"""
    raja_path = os.path.join(directory, ".raja")
    if os.path.isdir(raja_path):
        print(f"Raja workspace already exists at {os.path.abspath(raja_path)}")
        return
    os.mkdir(raja_path)
    open(os.path.join(raja_path, ".raja_files"), "w+").close()
    with open(os.path.join(raja_path, ".raja_settings.json"), "w+") as f:
        _base_settings["root"] = os.path.abspath(os.path.join(".raja"))
        json.dump(_base_settings, f, indent=4)
    print(f"Raja directory at {os.path.abspath(raja_path)} was initialized successfully")


def destroy(directory: str = ".") -> None:
    """Removes raja workspace from a given directory"""
    raja_path = os.path.join(directory, ".raja")
    if not os.path.isdir(raja_path):
        print(f"Raja workspace does not exists at {os.path.abspath(directory)}")
        return
    ans = input("Delete the raja workspace? [y\\N] ")
    if ans.lower() != "y":
        return
    shutil.rmtree(raja_path)
    print(f"Raja directory at {os.path.abspath(directory)} was destroyed successfully")
