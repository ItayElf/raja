from raja.changes_finder.changes.change import Change


class Subtract(Change):
    """Represent a subtraction of a character at a specific index"""

    def __init__(self, value: bytes, index: int):
        super().__init__(value, index)

    def reversed(self):
        from raja.changes_finder.changes.append import Append
        return Append(value=self.value, index=self.index)

    def encoded(self) -> bytes:
        return b"S" + self.value + str(self.index).encode()
