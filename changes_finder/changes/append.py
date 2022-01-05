from changes_finder.changes.change import Change


class Append(Change):
    """Represent an appending of a character at a specific index"""
    def __init__(self, value: bytes, index: int):
        super().__init__(value, index)

    def reversed(self):
        from changes_finder.changes.subtract import Subtract
        return Subtract(value=self.value, index=self.index)

    def encoded(self) -> bytes:
        return b"A" + self.value + str(self.index).encode()
