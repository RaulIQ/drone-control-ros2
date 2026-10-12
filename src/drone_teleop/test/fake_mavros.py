from dataclasses import dataclass
from threading import Event
from typing import final

from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from rclpy.node import Node


@final
@dataclass(frozen=True)
class FakeMavros:
    """Obedient autopilot that records steps and reports its state."""

    _steps: list[str]
    _state: State
    _flown: Event

    def attach(self, node: Node) -> None:
        publisher = node.create_publisher(State, '/mavros/state', 10)
        node.create_timer(0.05, lambda: publisher.publish(self._state))
        node.create_service(SetMode, '/mavros/set_mode', self._switch)
        node.create_service(CommandBool, '/mavros/cmd/arming', self._arm)
        node.create_service(CommandTOL, '/mavros/cmd/takeoff', self._ascend)

    def _switch(self, request: SetMode.Request, response: SetMode.Response) -> SetMode.Response:
        self._steps.append(request.custom_mode)
        self._state.mode = request.custom_mode
        return SetMode.Response(mode_sent=True)

    def _arm(
        self, request: CommandBool.Request, response: CommandBool.Response
    ) -> CommandBool.Response:
        self._steps.append('arm')
        self._state.armed = request.value
        return CommandBool.Response(success=True)

    def _ascend(
        self, request: CommandTOL.Request, response: CommandTOL.Response
    ) -> CommandTOL.Response:
        self._steps.append(f'ascend {request.altitude:.2f}')
        self._flown.set()
        return CommandTOL.Response(success=True)
