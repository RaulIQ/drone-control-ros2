from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import final

from drone_teleop.keyboard.steering import Steering
from mavros_msgs.msg import PositionTarget
from rclpy.publisher import Publisher
from std_msgs.msg import String


@final
@dataclass(frozen=True)
class Controls:
    """Keyboard of the pilot, turned into flight commands and velocity targets."""

    _steering: Steering
    _words: Mapping[int, str]
    _targets: Publisher[PositionTarget]
    _commands: Publisher[String]

    def press(self, key: int) -> None:
        if key in self._words:
            self._commands.publish(String(data=self._words[key]))

    def steer(self, held: Collection[int], released: Collection[int]) -> None:
        if self._steering.grips(held) or self._steering.grips(released):
            self._targets.publish(self._steering.target(held))
