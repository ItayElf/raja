import sqlite3
from typing import List

from raja.committer import Commit
from raja.committer.orm import insert_file_change, get_all_changes_commit

_get_all_commits_sql = """
SELECT id, author, message, last_hash, "timestamp"
FROM commits
ORDER BY timestamp DESC;
"""


def insert_commit(db_path: str, commit: Commit) -> None:
    """Insert a commit to the db"""
    with sqlite3.connect(db_path) as conn:
        c = conn.execute(
            "INSERT INTO commits(author, message, last_hash, \"timestamp\", hash) VALUES(?, ?, ?, ?, ?)",
            (commit.author, commit.message, commit.last_commit_hash, commit.timestamp, commit.hash))
        commit.idx = c.lastrowid
    for fc in commit.file_changes:
        insert_file_change(db_path, fc, commit.idx)


def get_commit_by_hash(db_path: str, commit_hash: str) -> Commit:
    """Returns a commit by its hash.
    :raises FileNotFoundError"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT id, author, message, last_hash, \"timestamp\" FROM commits WHERE hash=?", (commit_hash,))
        tup = c.fetchone()
        if not tup:
            raise FileNotFoundError(f"No commit with hash {commit_hash}")
        idx, author, message, last_hash, timestamp = tup
        changes = get_all_changes_commit(db_path, idx)
        return Commit(author, message, last_hash, changes, timestamp, idx)


def get_all_commits(db_path: str) -> List[Commit]:
    """Returns all commits in the db ordered by their timestamp from newest to oldest"""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(_get_all_commits_sql)
        lst = c.fetchall()
        res = []
        for tup in lst:
            idx, author, message, last_hash, timestamp = tup
            changes = get_all_changes_commit(db_path, idx)
            res.append(Commit(author, message, last_hash, changes, timestamp, idx))
        return res
