from dataclasses import dataclass
from typing import final

from drone_teleop.flight.maneuver import Maneuver
from drone_teleop.flight.vehicle import Vehicle


@final
@dataclass(frozen=True)
class Takeoff(Maneuver):
    """Climb from the ground, each step taken only after the previous one succeeds."""

    _vehicle: Vehicle
    _altitude: float

    def fly(self) -> None:
        self._vehicle.switch('GUIDED')
        self._vehicle.arm()
        self._vehicle.ascend(self._altitude)
