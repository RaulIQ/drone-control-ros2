from dataclasses import dataclass
from typing import Any, final

from drone_teleop.link import Link


@final
@dataclass(frozen=True)
class FakeLink(Link):
    """Link that records requests and answers them with one canned response."""

    _response: Any
    _requests: list[Any]

    def ask(self, request: Any) -> Any:
        self._requests.append(request)
        return self._response
