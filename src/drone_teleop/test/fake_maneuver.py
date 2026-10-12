from dataclasses import dataclass
from typing import final

from drone_teleop.maneuver import Maneuver
from drone_teleop.refusal import Refusal


@final
@dataclass(frozen=True)
class FakeManeuver(Maneuver):
    """Maneuver that records its flights or refuses to fly."""

    _refused: bool
    _flights: list[str]

    def fly(self) -> None:
        if self._refused:
            raise Refusal('Fake maneuver refused to fly')
        self._flights.append('flown')
