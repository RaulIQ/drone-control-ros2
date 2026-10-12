from queue import Empty, Queue
import random
from uuid import uuid4

from domain import Domain
from drone_teleop.controls import Controls
from drone_teleop.pair import Pair
from drone_teleop.steering import Steering
from hamcrest import assert_that, calling, equal_to, raises
from mavros_msgs.msg import PositionTarget
from rclpy.context import Context
from rclpy.qos import QoSDurabilityPolicy, QoSProfile
from std_msgs.msg import String


def test_publishes_word_of_pressed_key() -> None:
    word = uuid4().hex
    key = random.randint(9, 900)
    inbox: Queue[String] = Queue()
    lasting = QoSProfile(depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
    with Domain(random.randint(1, 100), Context()) as node:
        node.create_subscription(String, '/words', inbox.put, lasting)
        Controls(
            Steering(Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)),
            {key: word},
            node.create_publisher(PositionTarget, '/targets', lasting),
            node.create_publisher(String, '/words', lasting)
        ).press(key)
        heard = inbox.get(timeout=10.0).data
    assert_that(heard, equal_to(word), 'Controls did not publish the word of the pressed key')


def test_keeps_silent_on_unbound_key() -> None:
    inbox: Queue[String] = Queue()
    lasting = QoSProfile(depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
    with Domain(random.randint(1, 100), Context()) as node:
        node.create_subscription(String, '/words', inbox.put, lasting)
        Controls(
            Steering(Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)),
            {random.randint(9, 400): uuid4().hex},
            node.create_publisher(PositionTarget, '/targets', lasting),
            node.create_publisher(String, '/words', lasting)
        ).press(random.randint(500, 900))
        assert_that(
            calling(inbox.get).with_args(timeout=1.0),
            raises(Empty),
            'Controls did not keep silent on the unbound key'
        )


def test_publishes_velocity_while_key_is_held() -> None:
    speed = random.uniform(0.5, 5.0)
    inbox: Queue[PositionTarget] = Queue()
    lasting = QoSProfile(depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
    with Domain(random.randint(1, 100), Context()) as node:
        node.create_subscription(PositionTarget, '/targets', inbox.put, lasting)
        Controls(
            Steering(Pair(1, 2, speed), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)),
            {random.randint(9, 900): uuid4().hex},
            node.create_publisher(PositionTarget, '/targets', lasting),
            node.create_publisher(String, '/words', lasting)
        ).steer({1}, set())
        heard = inbox.get(timeout=10.0).velocity.x
    assert_that(heard, equal_to(speed), 'Controls did not publish velocity while key was held')


def test_publishes_halt_when_last_key_is_released() -> None:
    inbox: Queue[PositionTarget] = Queue()
    lasting = QoSProfile(depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
    with Domain(random.randint(1, 100), Context()) as node:
        node.create_subscription(PositionTarget, '/targets', inbox.put, lasting)
        Controls(
            Steering(
                Pair(1, 2, random.uniform(0.5, 5.0)),
                Pair(3, 4, 1.0),
                Pair(5, 6, 1.0),
                Pair(7, 8, 1.0)
            ),
            {random.randint(9, 900): uuid4().hex},
            node.create_publisher(PositionTarget, '/targets', lasting),
            node.create_publisher(String, '/words', lasting)
        ).steer(set(), {1})
        heard = inbox.get(timeout=10.0).velocity.x
    assert_that(heard, equal_to(0.0), 'Controls did not publish halt after the key release')


def test_keeps_silent_while_idle() -> None:
    inbox: Queue[PositionTarget] = Queue()
    lasting = QoSProfile(depth=10, durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)
    with Domain(random.randint(1, 100), Context()) as node:
        node.create_subscription(PositionTarget, '/targets', inbox.put, lasting)
        Controls(
            Steering(Pair(1, 2, 1.0), Pair(3, 4, 1.0), Pair(5, 6, 1.0), Pair(7, 8, 1.0)),
            {random.randint(9, 900): uuid4().hex},
            node.create_publisher(PositionTarget, '/targets', lasting),
            node.create_publisher(String, '/words', lasting)
        ).steer(set(), {random.randint(9, 900)})
        assert_that(
            calling(inbox.get).with_args(timeout=1.0),
            raises(Empty),
            'Controls did not keep silent while idle'
        )
