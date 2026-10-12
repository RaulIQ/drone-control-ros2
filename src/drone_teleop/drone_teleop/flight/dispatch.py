from collections.abc import Mapping
from dataclasses import dataclass
from typing import final

from drone_teleop.flight.maneuver import Maneuver
from drone_teleop.flight.refusal import Refusal
from rclpy.impl.rcutils_logger import RcutilsLogger
from std_msgs.msg import String


@final
@dataclass(frozen=True)
class Dispatch:
    """Desk that answers each command word with its maneuver and logs the outcome."""

    _maneuvers: Mapping[str, Maneuver]
    _log: RcutilsLogger

    def receive(self, command: String) -> None:
        if command.data in self._maneuvers:
            try:
                self._maneuvers[command.data].fly()
                self._log.info(f'Command {command.data} succeeded')
            except Refusal as refusal:
                self._log.error(f'Command {command.data} failed: {refusal}')
        else:
            self._log.error(f'Command {command.data} is unknown')
