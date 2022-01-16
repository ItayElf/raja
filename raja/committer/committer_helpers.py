from typing import List

from raja.changes_finder import CF
from raja.committer.classes import FileChange


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
