from dataclasses import dataclass
from typing import final

from drone_teleop.maneuver import Maneuver
from drone_teleop.vehicle import Vehicle


@final
@dataclass(frozen=True)
class Transition(Maneuver):
    """Handover of the flight to one autopilot mode, such as LAND or RTL."""

    _vehicle: Vehicle
    _mode: str

    def fly(self) -> None:
        self._vehicle.switch(self._mode)
