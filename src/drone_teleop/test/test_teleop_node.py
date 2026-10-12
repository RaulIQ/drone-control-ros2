import os
import random
import subprocess
import sys
from threading import Event

from domain import Domain
from hamcrest import assert_that, equal_to
from rclpy.context import Context


def test_offers_flight_commands() -> None:
    seen = Event()
    number = random.randint(1, 100)
    with Domain(number, Context()) as node:
        node.create_timer(
            0.2, lambda: seen.set() if node.count_publishers('/flight_command') else None
        )
        with subprocess.Popen(
            [sys.executable, '-c', 'from drone_teleop.teleop_node import main; main()'],
            env={**os.environ, 'ROS_DOMAIN_ID': str(number), 'SDL_VIDEODRIVER': 'dummy'},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) as process:
            offered = seen.wait(30.0)
            process.kill()
    assert_that(offered, equal_to(True), 'Teleop node did not offer flight commands')
