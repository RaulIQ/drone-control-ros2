from dataclasses import dataclass
from typing import final

from drone_teleop.flight.link import Link
from drone_teleop.flight.refusal import Refusal
from drone_teleop.flight.status import Status
from drone_teleop.flight.vehicle import Vehicle
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode


@final
@dataclass(frozen=True)
class MavrosVehicle(Vehicle):
    """ArduPilot aircraft that obeys through MAVROS and confirms through its state."""

    _mode: Link
    _arming: Link
    _takeoff: Link
    _status: Status

    def switch(self, mode: str) -> None:
        if not self._mode.ask(SetMode.Request(custom_mode=mode)).mode_sent:
            raise Refusal(f'Autopilot rejected the request for mode {mode}')
        self._status.expect(
            lambda state: state.mode == mode, f'Autopilot did not enter mode {mode}'
        )

    def arm(self) -> None:
        if not self._arming.ask(CommandBool.Request(value=True)).success:
            raise Refusal('Autopilot refused to arm')
        self._status.expect(lambda state: state.armed, 'Autopilot did not report armed motors')

    def ascend(self, altitude: float) -> None:
        if not self._takeoff.ask(CommandTOL.Request(altitude=altitude)).success:
            raise Refusal(f'Autopilot refused to take off to {altitude} meters')
