from drone_teleop.axis import Axis
from drone_teleop.controls import Controls
from drone_teleop.steering import Steering
from drone_teleop.strokes import Strokes
from mavros_msgs.msg import PositionTarget
import pygame
import rclpy
from std_msgs.msg import String


def main() -> None:
    rclpy.init()
    node = rclpy.create_node('teleop_node')
    speed = node.declare_parameter('speed', 2.0).value
    controls = Controls(
        Steering(
            Axis(pygame.KSCAN_W, pygame.KSCAN_S, speed),
            Axis(pygame.KSCAN_A, pygame.KSCAN_D, speed),
            Axis(
                pygame.KSCAN_SPACE,
                pygame.KSCAN_LSHIFT,
                node.declare_parameter('climb', 1.0).value
            ),
            Axis(pygame.KSCAN_Q, pygame.KSCAN_E, node.declare_parameter('turn', 1.0).value)
        ),
        {pygame.KSCAN_T: 'takeoff', pygame.KSCAN_L: 'land', pygame.KSCAN_R: 'rtl'},
        node.create_publisher(PositionTarget, '/mavros/setpoint_raw/local', 10),
        node.create_publisher(String, '/flight_command', 10)
    )
    pygame.init()
    pygame.display.set_caption('W/S A/D Space/Shift Q/E fly, T/L/R command')
    pygame.display.set_mode((480, 120))
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    clock = pygame.time.Clock()
    held: frozenset[int] = frozenset()
    try:
        while rclpy.ok() and not pygame.event.peek(pygame.QUIT):
            strokes = Strokes(pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)))
            for key in strokes.pressed():
                controls.press(key)
            held = (held | strokes.pressed()) - strokes.released()
            controls.steer(held, strokes.released())
            clock.tick(20)
    except KeyboardInterrupt:
        node.get_logger().info('Teleop node is stopping')
    finally:
        pygame.quit()
        rclpy.try_shutdown()
