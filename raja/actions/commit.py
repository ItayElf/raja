import json
import os
import sqlite3
import time

from raja.committer import create_commit, insert_commit
from raja.utils import error, success


def commit(message: str) -> None:
    """Commits the recent changes to the db"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    if not settings["username"]:
        error("Use 'raja config username <username>' before committing.")
        return
    t1 = time.time()
    files = open(os.path.join(".raja", ".raja_files")).read().split("\n")
    with sqlite3.connect(os.path.join(".raja", ".raja_db")) as conn:
        c = create_commit(files, conn, settings["username"], message, settings["last_commit"])
        insert_commit(conn, c)
    with open(os.path.join(".raja", ".raja_settings.json"), "w") as f:
        settings["last_commit"] = c.hash
        json.dump(settings, f, indent=2)
    t2 = time.time()
    success(f"{len(c.file_changes)} changes saved ( {round(t2 - t1, 2)} s)")
