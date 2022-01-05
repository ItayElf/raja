from __future__ import annotations

from abc import ABC, abstractmethod


class Change(ABC):
    """Abstract class for a change between two byte strings"""
    def __init__(self, value: bytes, index: int) -> None:
        self.value = value
        self.index = index

    @abstractmethod
    def reversed(self) -> Change:
        ...

    @abstractmethod
    def encoded(self) -> bytes:
        ...

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        for k in self.__dict__:
            if self.__dict__[k] != other.__dict__[k]:
                return False
        return True

    def __repr__(self):
        return f"{type(self).__name__}({', '.join([f'{key}: {val}' for key, val in self.__dict__.items()])})"
