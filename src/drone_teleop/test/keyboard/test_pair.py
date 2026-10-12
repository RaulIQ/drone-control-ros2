import random

from drone_teleop.keyboard.pair import Pair
from hamcrest import assert_that, equal_to


def test_pushes_forward_while_plus_key_is_held() -> None:
    plus = random.randint(1, 500)
    scale = random.uniform(0.5, 5.0)
    assert_that(
        Pair(plus, plus + 1, scale).value({plus, random.randint(600, 900)}),
        equal_to(scale),
        'Pair did not push forward while its plus key was held'
    )


def test_pushes_backward_while_minus_key_is_held() -> None:
    plus = random.randint(1, 500)
    scale = random.uniform(0.5, 5.0)
    assert_that(
        Pair(plus, plus + 1, scale).value({plus + 1}),
        equal_to(-scale),
        'Pair did not push backward while its minus key was held'
    )


def test_rests_while_both_keys_are_held() -> None:
    plus = random.randint(1, 500)
    assert_that(
        Pair(plus, plus + 1, random.uniform(0.5, 5.0)).value({plus, plus + 1}),
        equal_to(0.0),
        'Pair did not rest while both keys were held'
    )


def test_rests_while_foreign_keys_are_held() -> None:
    plus = random.randint(1, 500)
    assert_that(
        Pair(plus, plus + 1, random.uniform(0.5, 5.0)).value({random.randint(600, 900)}),
        equal_to(0.0),
        'Pair did not rest while only foreign keys were held'
    )


def test_grips_its_own_key() -> None:
    plus = random.randint(1, 500)
    assert_that(
        Pair(plus, plus + 1, random.uniform(0.5, 5.0)).grips({plus + 1}),
        equal_to(True),
        'Pair did not grip its own key'
    )


def test_does_not_grip_foreign_key() -> None:
    plus = random.randint(1, 500)
    assert_that(
        Pair(plus, plus + 1, random.uniform(0.5, 5.0)).grips({random.randint(600, 900)}),
        equal_to(False),
        'Pair did not let the foreign key go'
    )
