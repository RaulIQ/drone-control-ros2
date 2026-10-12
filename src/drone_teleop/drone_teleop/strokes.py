from collections.abc import Sequence
from dataclasses import dataclass
from typing import final

import pygame
from pygame.event import Event


@final
@dataclass(frozen=True)
class Strokes:
    """Key events read by position on the keyboard, whatever the layout."""

    _events: Sequence[Event]

    def pressed(self) -> frozenset[int]:
        return frozenset(
            event.scancode for event in self._events if event.type == pygame.KEYDOWN
        )

    def released(self) -> frozenset[int]:
        return frozenset(
            event.scancode for event in self._events if event.type == pygame.KEYUP
        )
