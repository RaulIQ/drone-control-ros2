import random

from drone_teleop.strokes import Strokes
from hamcrest import assert_that, equal_to
import pygame


def test_reads_pressed_key_by_position_under_foreign_layout() -> None:
    assert_that(
        Strokes(
            [pygame.event.Event(pygame.KEYDOWN, key=ord('ц'), scancode=pygame.KSCAN_W)]
        ).pressed(),
        equal_to({pygame.KSCAN_W}),
        'Strokes did not read the pressed key by its position'
    )


def test_reads_released_key_by_position_under_foreign_layout() -> None:
    assert_that(
        Strokes(
            [pygame.event.Event(pygame.KEYUP, key=ord('ф'), scancode=pygame.KSCAN_A)]
        ).released(),
        equal_to({pygame.KSCAN_A}),
        'Strokes did not read the released key by its position'
    )


def test_does_not_take_release_for_press() -> None:
    assert_that(
        Strokes(
            [pygame.event.Event(pygame.KEYUP, key=random.randint(1, 900), scancode=4)]
        ).pressed(),
        equal_to(set()),
        'Strokes did not tell the release from the press'
    )


def test_does_not_take_press_for_release() -> None:
    assert_that(
        Strokes(
            [pygame.event.Event(pygame.KEYDOWN, key=random.randint(1, 900), scancode=4)]
        ).released(),
        equal_to(set()),
        'Strokes did not tell the press from the release'
    )
