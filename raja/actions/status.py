import os
import sqlite3
import time

from raja.committer.orm import get_all_commits
from raja.utils import error
from rich.table import Table
from rich.console import Console


def status(*args) -> None:
    """Shows all the saved commits and how many files have been changes in each one"""
    full = "-a" in args
    if not os.path.isdir(".raja"):
        error("Raja was not initialized. Use 'raja init'")
        return
    with open(os.path.join(".raja", ".raja_files")) as f:
        filecount = len([v for v in f.read().split("\n") if v])
    with sqlite3.connect(os.path.join(".raja", ".raja_db")) as conn:
        commits = get_all_commits(conn)
    conn.close()
    t = Table(title=f"Commits (Newest to Latest, {filecount} Tracked Files)")
    t.add_column("Date", style="cyan")
    t.add_column("Hash", style="magenta")
    t.add_column("Comment", style="green")
    t.add_column("Author", style="#FF69B4")
    t.add_column("Files Changed", justify="right")
    for c in commits:
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(c.timestamp))
        commit_hash = c.hash if full else c.hash[:6] + "..."
        t.add_row(date, commit_hash, c.message, c.author,
                  f"{len(c.file_changes)} ({round(len(c.file_changes) * 100 / filecount)}%)")
    console = Console()
    console.print(t)
