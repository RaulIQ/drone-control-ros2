from collections.abc import Collection
from dataclasses import dataclass
from typing import final

from drone_teleop.keyboard.axis import Axis
from geometry_msgs.msg import Vector3
from mavros_msgs.msg import PositionTarget


@final
@dataclass(frozen=True)
class Steering:
    """Velocity relative to the nose of the drone that the held keys ask for."""

    _forward: Axis
    _left: Axis
    _up: Axis
    _turn: Axis

    def target(self, held: Collection[int]) -> PositionTarget:
        return PositionTarget(
            coordinate_frame=PositionTarget.FRAME_BODY_NED,
            type_mask=(
                PositionTarget.IGNORE_PX
                | PositionTarget.IGNORE_PY
                | PositionTarget.IGNORE_PZ
                | PositionTarget.IGNORE_AFX
                | PositionTarget.IGNORE_AFY
                | PositionTarget.IGNORE_AFZ
                | PositionTarget.IGNORE_YAW
            ),
            velocity=Vector3(
                x=self._forward.value(held), y=self._left.value(held), z=self._up.value(held)
            ),
            yaw_rate=self._turn.value(held)
        )

    def grips(self, keys: Collection[int]) -> bool:
        return any(
            axis.grips(keys) for axis in (self._forward, self._left, self._up, self._turn)
        )
