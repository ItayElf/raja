import json
import os
import shutil

from raja.committer.orm import init_db
from raja.utils import error, success

_base_settings = {
    "ignored_extensions": [],
    "ignored_directories": [],
    "ignored_files": [],
    "last_commit": None,
    "username": "",
    "token": "",
    "url": "",
}


def init(name: str = "") -> None:
    """Initialize raja workspace at the current working directory"""
    raja_path = os.path.join(".", ".raja")
    if os.path.isdir(raja_path):
        error(f"Raja workspace already exists at {raja_path}")
        return
    os.mkdir(raja_path)
    open(os.path.join(raja_path, ".raja_files"), "w+").close()
    with open(os.path.join(raja_path, ".raja_settings.json"), "w+") as f:
        _base_settings["workspace_name"] = name if name else os.getcwd().split(os.path.sep)[-1]
        json.dump(_base_settings, f, indent=2)
    init_db(os.path.join(raja_path, ".raja_db"))
    success(f"Raja workspace at {os.path.relpath(raja_path, '.')} was initialized successfully")


def destroy() -> None:
    """Removes raja workspace from a given directory"""
    raja_path = os.path.join(".", ".raja")
    if not os.path.isdir(raja_path):
        error(f"Raja workspace does not exists at the current working directory")
        return
    ans = input("Delete the raja workspace? [y\\N] ")
    if ans.lower() != "y":
        return
    shutil.rmtree(raja_path)
    success(f"Raja workspace was destroyed successfully")


def reset() -> None:
    """Reset a raja workspace"""
    raja_path = os.path.join(".", ".raja")
    if not os.path.isdir(raja_path):
        error(f"Raja workspace does not exists at the current working directory")
        return
    ans = input("Reset the raja workspace? [y\\N] ")
    if ans.lower() != "y":
        return
    with open(os.path.join(raja_path, ".raja_settings.json")) as f:
        data = json.load(f)
    name = data["workspace_name"]
    username = data["username"]
    shutil.rmtree(raja_path)
    os.mkdir(raja_path)
    open(os.path.join(raja_path, ".raja_files"), "w+").close()
    with open(os.path.join(raja_path, ".raja_settings.json"), "w+") as f:
        _base_settings["workspace_name"] = name
        _base_settings["username"] = username
        json.dump(_base_settings, f, indent=2)
    init_db(os.path.join(raja_path, ".raja_db"))
    success(f"Raja workspace was reset successfully")
