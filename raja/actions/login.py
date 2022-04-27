import json
import os
import getpass

import requests

from raja.constants import BASE_URL
from raja.utils import error, success


def login():
    """Generates an auth token"""
    raja_path = os.path.join(".", ".raja")
    if not os.path.isdir(raja_path):
        error(f"Raja workspace does not exists at the current working directory")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    if not settings["username"]:
        error("Use 'raja config username <username>' before committing.")
        return
    username = settings["username"]
    u = input(f"Enter username: [{username}]: ")
    if u:
        username = u
    password = getpass.getpass("Enter password: ")
    r = requests.post(BASE_URL + "auth/login", json={"username": username, "password": password}, verify=False)
    ans = json.loads(r.text)
    if not ans:
        error(f"Incorrect username or password. You can register on {BASE_URL.replace('/api', '') + '/signUp'}")
        return
    settings["token"] = ans
    with open(os.path.join(".raja", ".raja_settings.json"), "w") as f:
        json.dump(settings, f)
    success("Logged in successfully")
