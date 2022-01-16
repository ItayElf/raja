import sqlite3

_init_script = """
CREATE TABLE IF NOT EXISTS change_blobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    changes BLOB UNIQUE
);
CREATE TABLE IF NOT EXISTS commits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author text NOT NULL,
    message text NOT NULL,
    last_hash text, 
    timestamp INTEGER NOT NULL,
    hash text NOT NULL
);
CREATE TABLE IF NOT EXISTS file_changes(
    name text NOT NULL,
    change_id INTEGER NOT NULL,
    is_full INTEGER NOT NULL,
    commit_id INTEGER NOT NULL,
    FOREIGN KEY(change_id) REFERENCES change_blobs(id),
    FOREIGN KEY(commit_id) REFERENCES commits(id)
);
INSERT INTO change_blobs(changes) VALUES('');
"""


def init_db(db_path: str) -> None:
    """Initialize the .raja_db file"""
    with sqlite3.connect(db_path) as conn:
        conn.executescript(_init_script)
        conn.commit()
