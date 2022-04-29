import json
import os
import sqlite3

from raja.utils import error
from raja.committer import rollback as rb


def rollback(commit: str, path: str = "."):
    """Rolls back to the given commit and saved it to the given path, defaults to the current working dir"""
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_settings.json")) as f:
        settings = json.load(f)
    with sqlite3.connect(os.path.join(".raja", ".raja_db")) as conn:
        try:
            rb(conn, commit, path)
        except FileNotFoundError as e:
            error(str(e))
            return
    conn.close()
    settings["last_commit"] = commit
    with open(os.path.join(".raja", ".raja_settings.json"), "w") as f:
        json.dump(settings, f)
