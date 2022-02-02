from raja.changes_finder.changes.change import Change


class Delete(Change):
    """Represent a deletion of a file"""

    def __init__(self):
        super().__init__(b"", 0)

    def reversed(self):
        raise FileNotFoundError("Delete change")

    def encoded(self) -> bytes:
        return b"D"
