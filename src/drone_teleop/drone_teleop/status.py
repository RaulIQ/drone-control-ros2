from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from threading import Condition
from typing import final

from drone_teleop.refusal import Refusal
from mavros_msgs.msg import State


@final
@dataclass(frozen=True)
class Status:
    """Latest state reported by the autopilot, awaited for a bounded time."""

    _timeout: float
    _latest: deque[State] = field(default_factory=lambda: deque(maxlen=1))
    _change: Condition = field(default_factory=Condition)

    def record(self, state: State) -> None:
        with self._change:
            self._latest.append(state)
            self._change.notify_all()

    def expect(self, check: Callable[[State], bool], reason: str) -> None:
        with self._change:
            if not self._change.wait_for(lambda: any(map(check, self._latest)), self._timeout):
                raise Refusal(reason)
