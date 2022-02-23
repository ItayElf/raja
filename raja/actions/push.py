import base64
import json
import os
import requests
from raja.utils import error, success


def push():
    """Push the current committed project to the url in the settings"""
    raja_path = os.path.join(".", ".raja")
    if not os.path.isdir(raja_path):
        error(f"Raja workspace does not exists at the current working directory")
        return
    settings_path = os.path.join(".raja", ".raja_settings.json")
    with open(settings_path) as f:
        settings = json.load(f)
    if not settings["url"]:
        error("Use 'raja config url <url>' before committing.")
        return
    url = settings["url"]
    db_path = os.path.join(raja_path, ".raja_db")
    db = base64.b64encode(open(db_path, "rb").read()).hex()
    settings_file = base64.b64encode(open(settings_path, "rb").read()).hex()
    r = requests.post(
        url,
        json={"username": settings["username"], "token": settings["token"], "db": db, "settings": settings_file},
        verify=False,
        headers={"Content-Type": "application/json"}
    )
    if r.status_code != 200:
        error(r.text)
    else:
        success(f"Project pushed to {url} successfully")
