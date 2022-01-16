from __future__ import annotations

import os.path
from typing import List
from raja.changes_finder.changes import Replace, Subtract, Append, Change
from raja.changes_finder.cf_helpers import get_changes_bin2, get_changes_bin, parse_encoded, combine_encodeds, \
    get_changes_bin_file

_bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "dh_lin.exe")


class CF:
    """Class that compares two byte strings and detects the changes in form of replaces, appends or subtracts, allowing
    to apply those changes."""

    def __init__(self, previous: bytes, current: bytes) -> None:
        self._changes = get_changes_bin(_bin_path, previous, current)

    def apply(self, content: bytes, reverse: bool = False) -> bytes:
        """Applies the changes loaded onto the content, giving the new content from the previous or the opposite if reverse is True"""
        lst = list(content)
        changes = self._changes if not reverse else self._changes_reversed
        for change in changes:
            if isinstance(change, Replace):
                lst[change.index] = ord(change.value)
            elif isinstance(change, Subtract):
                del lst[change.index]
            elif isinstance(change, Append):
                lst.insert(change.index, ord(change.value))
        return b"".join([chr(val).encode() for val in lst])

    @classmethod
    def from_files(cls, previous_fname: str, current_fname: str) -> CF:
        """Returns a CF object from changes in the given files"""
        a = cls(b"", b"")
        a._changes = get_changes_bin2(_bin_path, previous_fname, current_fname)
        return a

    @classmethod
    def from_encoded(cls, encoded: bytes) -> CF:
        """Returns a CF object from encoded changes byte string"""
        a = cls(b"", b"")
        a._changes = parse_encoded(encoded)
        return a

    @classmethod
    def from_multiple_encoded(cls, encodeds: List[bytes]) -> CF:
        """Returns a CF object from list of encoded changes byte strings"""
        a = cls(b"", b"")
        a._changes = combine_encodeds(encodeds)
        return a

    @classmethod
    def from_file_and_data(cls, fname: str, data: bytes) -> CF:
        """Returns a CF object from file (which is the current) and data (previous)"""
        a = cls(b"", b"")
        a._changes = get_changes_bin_file(_bin_path, fname, data)
        return a

    @property
    def _changes_reversed(self) -> List[Change]:
        """Returns the reversed operations needed to be performed"""
        return [val.reversed() for val in self._changes][::-1]

    @property
    def encoded_changes(self) -> bytes:
        """Returns changes in a form of encoded string"""
        return b"".join([val.encoded() for val in self._changes])

    @property
    def no_change(self) -> bool:
        return not self._changes
