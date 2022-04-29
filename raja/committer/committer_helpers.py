import os.path
import sqlite3
import time
from typing import List, Optional, Dict

from raja.changes_finder import CF
from raja.committer.classes import FileChange, Commit
from raja.committer.orm import get_commit_by_hash, delete_commit_by_hash, get_all_changes_name, \
    get_all_changes_prior_to, cleanup, get_all_commits
from raja.file_handler.file_handler import get_all_files, generate_files_string


def _filter_file_changes(changes: List[FileChange]):
    """Removes all deletes if the file was created again"""
    if not changes or not changes[-1].is_full and changes[-1].changes == b"D":
        return changes
    lst = []
    for c in changes:
        if c.is_full or c.changes != b"D":
            lst.append(c)
    return lst


def get_full_file_content(changes: List[FileChange]) -> bytes:
    """Builds the file content from the given changes. changes must be sorted by chronological order, such that the first one is the newest"""
    file = b""
    # changes = _filter_file_changes(changes)
    for change in changes[::-1]:
        if change.is_full:
            file = change.changes
        else:
            cf = CF.from_encoded(change.changes)
            file = cf.apply(file)
    return file


def create_commit(files: List[str], conn: sqlite3.Connection, author: str, message: str,
                  last_hash: Optional[str]) -> Commit:
    """Creates a commit based on the tracked files"""
    changes = []
    for file in files:
        if not os.path.isfile(file):
            changes.append(FileChange(file, b"D", False))
            continue
        prev_changes = get_all_changes_name(conn, file)
        data = get_full_file_content(prev_changes)
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


def rollback(conn: sqlite3.Connection, commit: str, path: str = ".", ignored_extensions: List[str] = None,
             ignored_directories: List[str] = None, ignored_files: List[str] = None) -> str:
    """Goes back to the given commit and deletes the previous ones from db"""
    c = get_commit_by_hash(conn, commit)
    changes = get_all_changes_prior_to(conn, c.timestamp)
    grouped: Dict[str, List[FileChange]] = {}
    files = get_all_files(ignored_extensions=ignored_extensions, ignored_directories=ignored_directories,
                          ignored_files=ignored_files)
    for change in changes:
        if change.name in grouped:
            grouped[change.name].append(change)
        else:
            grouped[change.name] = [change]
    for file in grouped:
        try:
            save_full_path(os.path.join(path, file), get_full_file_content(grouped[file]))
        except FileNotFoundError:
            if os.path.isfile(file):
                os.unlink(file)
    for file in generate_files_string(files).split("\n"):
        if file and file not in grouped:
            os.unlink(file)
    commits = [v for v in get_all_commits(conn) if v.timestamp > c.timestamp]
    for commit in commits:
        delete_commit_by_hash(conn, commit.hash)
    cleanup(conn)
    return c.hash
