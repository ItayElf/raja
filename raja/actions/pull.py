import json
import os.path
import sqlite3

import requests

from raja.actions.add import add
from raja.committer import rollback as rb

from raja.utils import error, success


def pull():
    """Pulls the workspace from the server"""
    raja_path = os.path.join(".", ".raja")
    if not os.path.isdir(raja_path):
        error(f"Raja workspace does not exists at the current working directory")
        return
    settings_path = os.path.join(".raja", ".raja_settings.json")
    with open(settings_path) as f:
        settings = json.load(f)
    if not settings["base_url"]:
        error("Use 'raja config base_url <base_url>' before pushing.")
        return
    if not settings["url"]:
        repo = input(f"Name of the repo you want to pull: ")
        while not repo:
            repo = input(f"Name of the repo you want to pull: ")
        settings["url"] = settings["base_url"] + "/api/repos/" + repo
        with open(settings_path, "w") as f:
            json.dump(settings, f)
    url = settings["url"] + "/pull"
    r = requests.post(
        url,
        json={
            "username": settings["username"],
            "token": settings["token"]
        },
        verify=False,
        headers={"Content-Type": "application/json"},
    )
    if r.status_code != 200:
        error(r.text)
        return
    jsn = r.json()
    settings["ignored_extensions"] = jsn["settings"]["ignored_extensions"]
    settings["ignored_directories"] = jsn["settings"]["ignored_directories"]
    settings["ignored_files"] = jsn["settings"]["ignored_files"]
    settings["last_commit"] = jsn["settings"]["last_commit"]
    settings["base_url"] = jsn["settings"]["base_url"]
    settings["url"] = jsn["settings"]["url"]
    settings["workspace_name"] = jsn["settings"]["workspace_name"]
    with open(os.path.join(raja_path, ".raja_settings.json"), "w") as f:
        json.dump(settings, f)
    with open(os.path.join(raja_path, ".raja_db"), "wb") as f:
        f.write(b"".fromhex(jsn["db"]))
    with sqlite3.connect(os.path.join(raja_path, ".raja_db")) as conn:
        rb(conn, settings["last_commit"])
    open(os.path.join(raja_path, ".raja_files"), "w").close()
    add(".")
    success("Repo pulled successfully")
