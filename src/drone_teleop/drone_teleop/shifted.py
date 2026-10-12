from collections.abc import Collection
from dataclasses import dataclass
from typing import final

from drone_teleop.axis import Axis


@final
@dataclass(frozen=True)
class Shifted(Axis):
    """Axis pushed by one key and reversed while the shift is held with it."""

    _key: int
    _shift: int
    _scale: float

    def value(self, held: Collection[int]) -> float:
        return self._scale * (self._key in held) * (1 - 2 * (self._shift in held))

    def grips(self, keys: Collection[int]) -> bool:
        return self._key in keys
