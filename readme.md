# drone-control-ros2

Control of an ArduPilot drone from ROS 2 through MAVROS.

The `drone_teleop` package holds two nodes:

- `flight_manager` accepts the commands `takeoff`, `land`, and `rtl`, and carries them out on the autopilot step by step.
- `teleop_node` reads the keyboard, publishes velocities, and sends commands to `flight_manager`.

## Requirements

The project is tested on Ubuntu 26.04 with ROS 2 Lyrical.

1. ROS 2 Lyrical: the `ros-lyrical-desktop` or `ros-lyrical-ros-base` package.
2. MAVROS and its messages:

   ```bash
   sudo apt install ros-lyrical-mavros ros-lyrical-mavros-extras ros-lyrical-mavros-msgs
   ```

3. Geographic datasets for MAVROS, which does not start without them:

   ```bash
   sudo /opt/ros/lyrical/lib/mavros/install_geographiclib_datasets.sh
   ```

4. Python libraries: pygame for the keyboard window and Hamcrest for the tests:

   ```bash
   sudo apt install python3-pygame python3-hamcrest
   ```

5. An autopilot: the [ArduPilot SITL](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html) simulator or a real drone running ArduCopter.

## Build

```bash
cd ~/code/drone-control-ros2
source /opt/ros/lyrical/setup.bash
colcon build --packages-select drone_teleop
source install/setup.bash
```

Rebuild after every code change, and run `source install/setup.bash` in every new terminal.

## Run

Start each program in its own terminal, in this order.

1. The simulator:

   ```bash
   sim_vehicle.py -v ArduCopter
   ```

2. MAVROS. The address must match the one where the simulator sends MAVLink, which is port 14550 by default:

   ```bash
   ros2 launch mavros apm.launch fcu_url:=udp://127.0.0.1:14550@
   ```

   The link is up when the command below shows `connected: true`:

   ```bash
   ros2 topic echo /mavros/state --once
   ```

3. The flight manager:

   ```bash
   ros2 run drone_teleop flight_manager
   ```

4. The keyboard control:

   ```bash
   ros2 run drone_teleop teleop_node
   ```

## Controls

The keys work while the `teleop_node` window has focus.

| Keys | Action |
| --- | --- |
| `T` | take off |
| `L` | land in place |
| `R` | return to the launch point |
| `W` / `S` | forward / backward |
| `A` / `D` | left / right |
| `Space` / left `Shift` + `Space` | up / down |
| `Q` / `E` | turn left / right |

Motion is relative to the nose of the drone and works only after a takeoff through `T`.

Commands can also be sent without the keyboard:

```bash
ros2 topic pub --once /flight_command std_msgs/msg/String "{data: takeoff}"
```

`flight_manager` logs the outcome of every command. When a step fails, the message names the step and the reason.

## Parameters

| Node | Parameter | Default | Meaning |
| --- | --- | --- | --- |
| `flight_manager` | `altitude` | 7.0 | takeoff altitude, m |
| `teleop_node` | `speed` | 2.0 | horizontal speed, m/s |
| `teleop_node` | `climb` | 1.0 | vertical speed, m/s |
| `teleop_node` | `turn` | 1.0 | turn rate, rad/s |

Example:

```bash
ros2 run drone_teleop flight_manager --ros-args -p altitude:=9.0
```

## Tests

```bash
cd src/drone_teleop
python3 -m pytest test
```

The tests need neither the simulator nor MAVROS: a fake stands in for the autopilot.
