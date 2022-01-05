from changes_finder.changes.change import Change


class Replace(Change):
    """Represents a replacement of one byte with another between two byte strings"""
    def __init__(self, value: bytes, index: int, prev: bytes):
        super().__init__(value, index)
        self.prev = prev

    def reversed(self):
        return Replace(self.prev, self.index, self.value)

    def encoded(self) -> bytes:
        if self.prev == self.value:
            return b""
        return b"R" + b"".join([self.value, self.prev]) + str(self.index).encode()
