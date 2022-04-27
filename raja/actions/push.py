import base64
import json
import os
import requests
from raja.utils import error, success


# BASE_URL = "https://192.168.1.16:5000/api/repos/"


def push():
    """Push the current committed project to the url in the settings"""
    try:
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
        new = False
        if not settings["url"]:
            new = True
            repo = input(f"Name for new repo [{settings['workspace_name']}]: ")
            if not repo:
                repo = settings['workspace_name']
            settings["url"] = settings["base_url"] + "/api/repos/" + repo
            with open(settings_path, "w") as f:
                json.dump(settings, f)
        url = settings["url"]
        db_path = os.path.join(raja_path, ".raja_db")
        db = base64.b64encode(open(db_path, "rb").read()).hex()
        settings_file = base64.b64encode(open(settings_path, "rb").read()).hex()
        r = requests.post(
            url,
            json={"username": settings["username"], "token": settings["token"], "db": db, "settings": settings_file,
                  "new": new},
            verify=False,
            headers={"Content-Type": "application/json"}
        )
        if r.status_code != 200:
            error(r.text)
            if r.status_code == 406:
                settings["url"] = ""
                with open(settings_path, "w") as f:
                    json.dump(settings, f)
            elif r.status_code == 404 and "No repository with name" in r.text:
                if not new:
                    res = input("Create new repo instead? [y/N]")
                    if res.lower() == "y":
                        settings["url"] = ""
                        new = True
                if not new:
                    new_name = input("Try a new name: ")
                    settings["url"] = settings["base_url"] + "/api/repos/" + new_name
                with open(settings_path, "w") as f:
                    json.dump(settings, f)
                push()
        else:
            success(f"Project pushed to {url} successfully")
    except KeyboardInterrupt:
        exit()
