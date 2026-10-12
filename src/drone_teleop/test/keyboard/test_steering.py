import random

from drone_teleop.keyboard.pair import Pair
from drone_teleop.keyboard.steering import Steering
from hamcrest import assert_that, equal_to
from mavros_msgs.msg import PositionTarget


def test_flies_forward_at_axis_speed() -> None:
    speed = random.uniform(0.5, 5.0)
    assert_that(
        Steering(
            Pair(1, 2, speed), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).target({1}).velocity.x,
        equal_to(speed),
        'Steering did not fly forward at the axis speed'
    )


def test_flies_right_as_negative_left() -> None:
    speed = random.uniform(0.5, 5.0)
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, speed), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).target({4}).velocity.y,
        equal_to(-speed),
        'Steering did not fly right as negative left'
    )


def test_climbs_at_axis_speed() -> None:
    speed = random.uniform(0.5, 5.0)
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, speed), Pair(7, 8, 1.0)
        ).target({5}).velocity.z,
        equal_to(speed),
        'Steering did not climb at the axis speed'
    )


def test_turns_at_axis_rate() -> None:
    rate = random.randint(1, 40) / 8
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, rate)
        ).target({7}).yaw_rate,
        equal_to(rate),
        'Steering did not turn at the axis rate'
    )


def test_stands_still_without_keys() -> None:
    target = Steering(
        Pair(1, 2, random.uniform(0.5, 5.0)),
        Pair(3, 4, random.uniform(0.5, 5.0)),
        Pair(5, 6, random.uniform(0.5, 5.0)),
        Pair(7, 8, random.uniform(0.5, 5.0))
    ).target(set())
    assert_that(
        [target.velocity.x, target.velocity.y, target.velocity.z, target.yaw_rate],
        equal_to([0.0, 0.0, 0.0, 0.0]),
        'Steering did not stand still without keys'
    )


def test_speaks_in_body_frame() -> None:
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).target({1}).coordinate_frame,
        equal_to(PositionTarget.FRAME_BODY_NED),
        'Steering did not speak in the body frame'
    )


def test_asks_only_for_velocity_and_turn_rate() -> None:
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).target({1}).type_mask,
        equal_to(1479),
        'Steering did not mask everything except velocity and turn rate'
    )


def test_grips_key_of_any_axis() -> None:
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).grips({random.randint(1, 8)}),
        equal_to(True),
        'Steering did not grip the key of its axis'
    )


def test_does_not_grip_foreign_key() -> None:
    assert_that(
        Steering(
            Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)
        ).grips({random.randint(9, 900)}),
        equal_to(False),
        'Steering did not let the foreign key go'
    )
