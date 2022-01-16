from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import md5
from typing import List, Optional


@dataclass
class FileChange:
    """Represents a change to a file"""
    name: str
    changes: bytes
    is_full: bool  # True if the whole file was saved rather than only the changes


@dataclass
class Commit:
    """Represents a commit made by the user"""
    author: str
    message: str
    last_commit_hash: Optional[str]
    file_changes: List[FileChange]
    timestamp: int  # int(time.time())
    hash: str = field(init=False)
    idx: int = -1

    def __post_init__(self):
        self.hash = md5((f"{self.author}{self.message}{self.last_commit_hash}{self.timestamp}".encode())).hexdigest()
