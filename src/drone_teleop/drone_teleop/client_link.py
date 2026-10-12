from dataclasses import dataclass
from typing import Any, final

from drone_teleop.link import Link
from drone_teleop.refusal import Refusal
from rclpy.client import Client


@final
@dataclass(frozen=True)
class ClientLink(Link):
    """Link through a ROS service client that never waits beyond its timeout."""

    _client: Client[Any, Any]
    _timeout: float

    def ask(self, request: Any) -> Any:
        if not self._client.wait_for_service(self._timeout):
            raise Refusal(f'Service {self._client.service_name} is absent')
        try:
            return self._client.call(request, self._timeout)
        except TimeoutError as error:
            raise Refusal(
                f'Service {self._client.service_name} kept silent for {self._timeout} seconds'
            ) from error
