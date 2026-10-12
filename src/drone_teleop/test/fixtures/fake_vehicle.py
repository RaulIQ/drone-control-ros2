from dataclasses import dataclass
from typing import final

from drone_teleop.flight.refusal import Refusal
from drone_teleop.flight.vehicle import Vehicle


@final
@dataclass(frozen=True)
class FakeVehicle(Vehicle):
    """Vehicle that records obeyed steps and refuses the chosen ones."""

    _refused: frozenset[str]
    _steps: list[str]

    def switch(self, mode: str) -> None:
        self._obey('switch', f'switch {mode}')

    def arm(self) -> None:
        self._obey('arm', 'arm')

    def ascend(self, altitude: float) -> None:
        self._obey('ascend', f'ascend {altitude}')

    def _obey(self, step: str, record: str) -> None:
        if step in self._refused:
            raise Refusal(f'Fake vehicle refused to {step}')
        self._steps.append(record)
