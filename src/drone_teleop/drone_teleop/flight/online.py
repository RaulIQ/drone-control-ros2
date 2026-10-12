from dataclasses import dataclass
from typing import final

from drone_teleop.flight.status import Status
from drone_teleop.flight.vehicle import Vehicle


@final
@dataclass(frozen=True)
class Online(Vehicle):
    """Vehicle that obeys only while the autopilot stays connected."""

    _origin: Vehicle
    _status: Status

    def switch(self, mode: str) -> None:
        self._status.expect(lambda state: state.connected, 'Autopilot is not connected')
        self._origin.switch(mode)

    def arm(self) -> None:
        self._status.expect(lambda state: state.connected, 'Autopilot is not connected')
        self._origin.arm()

    def ascend(self, altitude: float) -> None:
        self._status.expect(lambda state: state.connected, 'Autopilot is not connected')
        self._origin.ascend(altitude)
