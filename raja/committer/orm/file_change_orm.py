import sqlite3
from typing import List

from raja.committer import FileChange

_get_file_sql = """
SELECT fc.name, cb.changes, fc.is_full 
FROM file_changes fc 
INNER JOIN change_blobs cb ON cb.id=fc.change_id
WHERE fc.name=? AND fc.commit_id=?;
"""

_get_changes_commit_sql = """
SELECT fc.name, cb.changes, fc.is_full 
FROM file_changes fc 
INNER JOIN change_blobs cb ON cb.id=fc.change_id
WHERE fc.commit_id=?;
"""

_get_changes_name_sql = """
SELECT fc.name, cb.changes, fc.is_full
FROM file_changes fc 
INNER JOIN change_blobs cb ON cb.id=fc.change_id
INNER JOIN commits cm ON cm.id=fc.commit_id
WHERE fc.name=?
ORDER BY cm."timestamp" DESC;
"""

_insert_file_change_sql = """
INSERT INTO file_changes(name, change_id, is_full, commit_id) 
SELECT ?, cb.id, ?, ? 
FROM change_blobs cb WHERE cb.changes=?
"""


def get_file_change(conn: sqlite3.Connection, name: str, commit_id: int) -> FileChange:
    """Returns a file change from its name and commit
    :raise FileNotFoundError"""
    c = conn.cursor()
    c.execute(_get_file_sql, (name, commit_id))
    tup = c.fetchone()
    if not tup:
        raise FileNotFoundError(f"No file change with name {name} and commit id {commit_id}")
    return FileChange(name, tup[1], bool(tup[2]))


def get_all_changes_commit(conn: sqlite3.Connection, commit_id: int) -> List[FileChange]:
    """Returns all changes for a commit"""
    c = conn.cursor()
    c.execute(_get_changes_commit_sql, (commit_id,))
    lst = c.fetchall()
    if lst:
        lst = [FileChange(name, changes, bool(is_full)) for name, changes, is_full in lst]
    return lst


def get_all_changes_name(conn: sqlite3.Connection, name: str) -> List[FileChange]:
    """Returns all changes made to a file over time from newest to oldest"""
    c = conn.cursor()
    c.execute(_get_changes_name_sql, (name,))
    lst = c.fetchall()
    if lst:
        lst = [FileChange(name, changes, bool(is_full)) for name, changes, is_full in lst]
    return lst


def _insert_change(conn: sqlite3.Connection, blob: bytes) -> None:
    """Inserts a blob to the changes if not exists"""
    try:
        conn.execute("INSERT INTO change_blobs(changes) VALUES(?)", (blob,))
        conn.commit()
    except sqlite3.IntegrityError:  # blob already exists
        return


def insert_file_change(conn: sqlite3.Connection, fc: FileChange, commit_id: int) -> None:
    """Inserts a file change to the db"""
    _insert_change(conn, fc.changes)
    conn.execute(_insert_file_change_sql, (fc.name, int(fc.is_full), commit_id, fc.changes))
    conn.commit()
