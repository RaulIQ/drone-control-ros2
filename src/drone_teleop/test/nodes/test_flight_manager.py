import os
import random
import subprocess
import sys
from threading import Event

from domain import Domain
from fake_mavros import FakeMavros
from hamcrest import assert_that, contains_exactly
from mavros_msgs.msg import State
from rclpy.context import Context
from std_msgs.msg import String


def test_takes_off_on_command() -> None:
    steps: list[str] = []
    flown = Event()
    number = random.randint(1, 100)
    altitude = random.uniform(5.0, 10.0)
    with Domain(number, Context()) as node:
        FakeMavros(steps, State(connected=True), flown).attach(node)
        publisher = node.create_publisher(String, '/flight_command', 10)
        node.create_timer(0.5, lambda: publisher.publish(String(data='takeoff')))
        with subprocess.Popen(
            [
                sys.executable,
                '-c',
                'from drone_teleop.nodes.flight_manager import main; main()',
                '--ros-args',
                '-p',
                f'altitude:={altitude}'
            ],
            env={**os.environ, 'ROS_DOMAIN_ID': str(number)},
            stderr=subprocess.DEVNULL
        ) as process:
            flown.wait(30.0)
            process.kill()
    assert_that(
        steps[:3],
        contains_exactly('GUIDED', 'arm', f'ascend {altitude:.2f}'),
        'Flight manager did not take off on command'
    )
