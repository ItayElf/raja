import os.path
import sqlite3
import time
from typing import List, Optional, Dict

from raja.changes_finder import CF
from raja.committer.classes import FileChange, Commit
from raja.committer.orm import get_commit_by_hash, delete_commit_by_hash, get_all_changes_name, \
    get_all_changes_prior_to, cleanup, get_all_commits


def get_full_file_content(changes: List[FileChange], current_content: bytes) -> bytes:
    """Builds the file content from the given changes. changes must be sorted by chronological order, such that the first one is the newest"""
    file = current_content
    for change in changes[::-1]:
        if change.is_full:
            file = change.changes
        else:
            cf = CF.from_encoded(change.changes)
            file = cf.apply(file, True)
    return file


def create_commit(files: List[str], conn: sqlite3.Connection, author: str, message: str,
                  last_hash: Optional[str]) -> Commit:
    """Creates a commit based on the tracked files"""
    changes = []
    for file in files:
        if not os.path.isfile(file):
            continue
        prev_changes = get_all_changes_name(conn, file)
        data = get_full_file_content(prev_changes, b"")
        cf = CF.from_file_and_data(file, data)
        if cf.no_change:
            continue
        if len(cf.encoded_changes) < cf.current_len:
            changes.append(FileChange(file, cf.encoded_changes, False))
        else:
            content = open(file, "rb").read()
            changes.append(FileChange(file, content, True))
    return Commit(author, message, last_hash, changes, int(time.time()))


def save_full_path(path: str, content: bytes) -> None:
    """saves a path and creates missing dirs"""
    splt = path.split(os.path.sep)
    for i in range(1, len(splt)):
        p = os.path.join(*splt[:i])
        if not os.path.isdir(p):
            os.mkdir(p)
    with open(path, "wb+") as f:
        f.write(content)


def rollback(conn: sqlite3.Connection, commit: str, path: str = ".") -> None:
    """Goes back to the given commit and deletes the previous ones from db"""
    c = get_commit_by_hash(conn, commit)
    changes = get_all_changes_prior_to(conn, c.timestamp)
    grouped: Dict[str, List[FileChange]] = {}
    for change in changes:
        if change.name in grouped:
            grouped[change.name].append(change)
        else:
            grouped[change.name] = [change]
    for file in grouped:
        save_full_path(os.path.join(path, file), get_full_file_content(grouped[file], b""))
    commits = [v for v in get_all_commits(conn) if v.timestamp > c.timestamp]
    for commit in commits:
        delete_commit_by_hash(conn, commit.hash)
    cleanup(conn)
