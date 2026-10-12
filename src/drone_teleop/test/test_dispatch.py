from uuid import uuid4

from drone_teleop.dispatch import Dispatch
from fake_maneuver import FakeManeuver
from hamcrest import assert_that, contains_exactly, empty
from rclpy.logging import get_logger, LoggingSeverity
from std_msgs.msg import String


def test_flies_maneuver_named_by_command() -> None:
    flights: list[str] = []
    word = uuid4().hex
    log = get_logger(uuid4().hex)
    log.set_level(LoggingSeverity.FATAL)
    Dispatch(
        {word: FakeManeuver(False, flights), uuid4().hex: FakeManeuver(True, [])}, log
    ).receive(String(data=word))
    assert_that(
        flights, contains_exactly('flown'), 'Dispatch did not fly the maneuver named by command'
    )


def test_does_not_fly_on_unknown_command() -> None:
    flights: list[str] = []
    log = get_logger(uuid4().hex)
    log.set_level(LoggingSeverity.FATAL)
    Dispatch({uuid4().hex: FakeManeuver(False, flights)}, log).receive(String(data=uuid4().hex))
    assert_that(flights, empty(), 'Dispatch did not ignore the unknown command')


def test_keeps_flying_after_refused_maneuver() -> None:
    flights: list[str] = []
    refused = uuid4().hex
    word = uuid4().hex
    log = get_logger(uuid4().hex)
    log.set_level(LoggingSeverity.FATAL)
    dispatch = Dispatch(
        {refused: FakeManeuver(True, []), word: FakeManeuver(False, flights)}, log
    )
    dispatch.receive(String(data=refused))
    dispatch.receive(String(data=word))
    assert_that(
        flights, contains_exactly('flown'), 'Dispatch did not keep flying after the refusal'
    )
