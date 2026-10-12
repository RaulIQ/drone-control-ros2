from drone_teleop.axis import Axis
from drone_teleop.controls import Controls
from drone_teleop.steering import Steering
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
            Axis(pygame.K_w, pygame.K_s, speed),
            Axis(pygame.K_a, pygame.K_d, speed),
            Axis(pygame.K_SPACE, pygame.K_LSHIFT, node.declare_parameter('climb', 1.0).value),
            Axis(pygame.K_q, pygame.K_e, node.declare_parameter('turn', 1.0).value)
        ),
        {pygame.K_t: 'takeoff', pygame.K_l: 'land', pygame.K_r: 'rtl'},
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
            pressed = frozenset(event.key for event in pygame.event.get(pygame.KEYDOWN))
            released = frozenset(event.key for event in pygame.event.get(pygame.KEYUP))
            for key in pressed:
                controls.press(key)
            held = (held | pressed) - released
            controls.steer(held, released)
            clock.tick(20)
    except KeyboardInterrupt:
        node.get_logger().info('Teleop node is stopping')
    finally:
        pygame.quit()
        rclpy.try_shutdown()
