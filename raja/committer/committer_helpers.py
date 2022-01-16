import os.path
import sqlite3
import time
from typing import List, Optional

from raja.changes_finder import CF
from raja.committer.classes import FileChange, Commit
from raja.committer.orm.file_change_orm import get_all_changes_name


def get_full_file_content(changes: List[FileChange], current_content: bytes) -> bytes:
    """Builds the file content from the given changes. changes must be sorted by chronological order, such that the first one is the newest"""
    file = current_content
    for change in changes:
        print(f"file: {file}")
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
