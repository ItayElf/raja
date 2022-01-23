import sqlite3
import zlib
from typing import List, Tuple

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

_get_changes_prior_to = """
SELECT fc.name, cb.changes, fc.is_full
FROM file_changes fc
INNER JOIN change_blobs cb ON cb.id=fc.change_id
INNER JOIN commits cm ON cm.id=fc.commit_id
WHERE cm."timestamp" <= ?
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
    return FileChange(name, zlib.decompress(tup[1]), bool(tup[2]))


def get_all_changes_commit(conn: sqlite3.Connection, commit_id: int) -> List[FileChange]:
    """Returns all changes for a commit"""
    c = conn.cursor()
    c.execute(_get_changes_commit_sql, (commit_id,))
    lst = c.fetchall()
    res = []
    for (name, change, is_full) in lst:
        change = zlib.decompress(change)
        is_full = not not is_full
        res.append(FileChange(name, change, is_full))
    return res


def get_all_changes_name(conn: sqlite3.Connection, name: str) -> List[FileChange]:
    """Returns all changes made to a file over time from newest to oldest"""
    c = conn.cursor()
    c.execute(_get_changes_name_sql, (name,))
    lst = c.fetchall()
    res = []
    for (name, change, is_full) in lst:
        change = zlib.decompress(change)
        is_full = not not is_full
        res.append(FileChange(name, change, is_full))
    return res


def get_all_changes_prior_to(conn: sqlite3.Connection, timestamp: int) -> List[FileChange]:
    """Returns all changes prior to the given timestamp (inclusive)"""
    c = conn.cursor()
    c.execute(_get_changes_prior_to, (timestamp,))
    lst = c.fetchall()
    res = []
    for (name, change, is_full) in lst:
        change = zlib.decompress(change)
        is_full = not not is_full
        res.append(FileChange(name, change, is_full))
    return res


def get_all_file_changes(conn: sqlite3.Connection) -> List[FileChange]:
    """Returns all file changes"""
    return get_all_changes_prior_to(conn, 9223372036854775807)


def _insert_change(conn: sqlite3.Connection, blob: bytes) -> int:
    """Inserts a blob to the changes if not exists and returns its id"""
    try:
        c = conn.execute("INSERT INTO change_blobs(changes) VALUES(?)", (zlib.compress(blob),))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:  # blob already exists
        c = conn.cursor()
        c.execute("SELECT id FROM change_blobs WHERE changes=?", (zlib.compress(blob),))
        return c.fetchone()[0]


def _get_all_blobs(conn: sqlite3.Connection) -> List[Tuple[int, bytes]]:
    """Returns a list of all blobs"""
    c = conn.cursor()
    c.execute("SELECT id, changes FROM change_blobs")
    return [(idx, zlib.decompress(blob)) for (idx, blob) in c.fetchall()]


def _delete_blob(conn: sqlite3.Connection, idx: int) -> None:
    """Deletes a blob from the db"""
    conn.execute("DELETE FROM change_blobs WHERE id=?", (idx,))
    conn.commit()


def insert_file_change(conn: sqlite3.Connection, fc: FileChange, commit_id: int) -> None:
    """Inserts a file change to the db"""
    idx = _insert_change(conn, fc.changes)
    conn.execute("INSERT INTO file_changes(name, change_id, is_full, commit_id) VALUES(?,?,?,?)",
                 (fc.name, idx, int(fc.is_full), commit_id))
    conn.commit()


def delete_file_change(conn: sqlite3.Connection, name: str, commit_idx: int) -> None:
    """Deletes a file change from the db"""
    conn.execute("DELETE FROM file_changes WHERE name=? AND commit_id=?", (name, commit_idx))
    conn.commit()


def cleanup(conn: sqlite3.Connection) -> None:
    """Deletes all unused blobs"""
    from raja.committer.orm import get_all_commits
    commits_idxs = {c.idx for c in get_all_commits(conn)}
    c = conn.cursor()
    c.execute("SELECT commit_id, name FROM file_changes")
    files = c.fetchall()
    for f in files:
        if f[0] not in commits_idxs:
            delete_file_change(conn, f[1], f[0])
    changes = {v.changes for v in get_all_file_changes(conn)}
    blobs = _get_all_blobs(conn)
    for b in blobs:
        if b[1] not in changes:
            _delete_blob(conn, b[0])
