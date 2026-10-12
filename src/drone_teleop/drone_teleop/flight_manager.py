from drone_teleop.client_link import ClientLink
from drone_teleop.dispatch import Dispatch
from drone_teleop.mavros_vehicle import MavrosVehicle
from drone_teleop.online import Online
from drone_teleop.status import Status
from drone_teleop.takeoff import Takeoff
from drone_teleop.transition import Transition
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from std_msgs.msg import String


def main() -> None:
    rclpy.init()
    node = rclpy.create_node('flight_manager')
    status = Status(10.0)
    vehicle = Online(
        MavrosVehicle(
            ClientLink(node.create_client(SetMode, '/mavros/set_mode'), 10.0),
            ClientLink(node.create_client(CommandBool, '/mavros/cmd/arming'), 10.0),
            ClientLink(node.create_client(CommandTOL, '/mavros/cmd/takeoff'), 10.0),
            status
        ),
        status
    )
    node.create_subscription(State, '/mavros/state', status.record, 10)
    node.create_subscription(
        String,
        '/flight_command',
        Dispatch(
            {
                'takeoff': Takeoff(vehicle, node.declare_parameter('altitude', 7.0).value),
                'land': Transition(vehicle, 'LAND'),
                'rtl': Transition(vehicle, 'RTL')
            },
            node.get_logger()
        ).receive,
        10,
        callback_group=MutuallyExclusiveCallbackGroup()
    )
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        node.get_logger().info('Flight manager is stopping')
    finally:
        rclpy.try_shutdown()
