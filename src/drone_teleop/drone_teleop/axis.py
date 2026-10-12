from abc import ABC, abstractmethod
from collections.abc import Collection


class Axis(ABC):
    """One direction of motion that held keys push either way."""

    @abstractmethod
    def value(self, held: Collection[int]) -> float:
        pass

    @abstractmethod
    def grips(self, keys: Collection[int]) -> bool:
        pass
