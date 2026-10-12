import random

from drone_teleop.keyboard.shifted import Shifted
from hamcrest import assert_that, equal_to


def test_pushes_forward_while_key_is_held_alone() -> None:
    key = random.randint(1, 500)
    scale = random.uniform(0.5, 5.0)
    assert_that(
        Shifted(key, key + 1, scale).value({key, random.randint(600, 900)}),
        equal_to(scale),
        'Shifted did not push forward while its key was held alone'
    )


def test_pushes_backward_while_key_is_held_with_shift() -> None:
    key = random.randint(1, 500)
    scale = random.uniform(0.5, 5.0)
    assert_that(
        Shifted(key, key + 1, scale).value({key, key + 1}),
        equal_to(-scale),
        'Shifted did not push backward while its key was held with shift'
    )


def test_rests_while_shift_is_held_alone() -> None:
    key = random.randint(1, 500)
    assert_that(
        Shifted(key, key + 1, random.uniform(0.5, 5.0)).value({key + 1}),
        equal_to(0.0),
        'Shifted did not rest while shift was held alone'
    )


def test_grips_its_key() -> None:
    key = random.randint(1, 500)
    assert_that(
        Shifted(key, key + 1, random.uniform(0.5, 5.0)).grips({key}),
        equal_to(True),
        'Shifted did not grip its key'
    )


def test_does_not_grip_lonely_shift() -> None:
    key = random.randint(1, 500)
    assert_that(
        Shifted(key, key + 1, random.uniform(0.5, 5.0)).grips({key + 1}),
        equal_to(False),
        'Shifted did not let the lonely shift go'
    )
