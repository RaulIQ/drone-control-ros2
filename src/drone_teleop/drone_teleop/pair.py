from collections.abc import Collection
from dataclasses import dataclass
from typing import final

from drone_teleop.axis import Axis


@final
@dataclass(frozen=True)
class Pair(Axis):
    """Axis pushed either way by a pair of opposing keys."""

    _plus: int
    _minus: int
    _scale: float

    def value(self, held: Collection[int]) -> float:
        return self._scale * ((self._plus in held) - (self._minus in held))

    def grips(self, keys: Collection[int]) -> bool:
        return self._plus in keys or self._minus in keys
