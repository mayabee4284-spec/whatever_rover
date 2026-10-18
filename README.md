
# Whatever Rover — Project Altair (Phase 3)

Autonomous waypoint navigation, telemetry monitoring, and safety interruption control package built for **Project Altair** using ROS 2 and Turtlesim.

---

## 📋 Environment & Compatibility
* **Operating System**: Ubuntu (Tested on 24.04 LTS / WSL2)
* **ROS 2 Distribution**: ROS 2 Jazzy Jalisco
* **Simulator**: Turtlesim
* **Python Version**: 3.10+

---

## 🚀 Features & Architecture

This repository contains the `rover_telemetry` ROS 2 package, featuring:
1. **Autonomous Waypoint Navigation (Task 3)**: Autonomous driving through predefined field locations (**Bottle** `[8.0, 5.5]`, **Mallet** `[8.0, 8.0]`, and **Base** `[5.5, 5.5]`) using proportional ($P$) position feedback control with a 0.3-unit arrival tolerance.
2. **Safety Interruption Handling**: Subscribes to the `/field_blocked` topic to immediately halt the rover when a hazard is reported, keeping it paused securely without discarding the target.
3. **Explicit Service Resumption**: Implements the `/resume_mission` trigger service, ensuring the mission cannot auto-resume when a blockage clears and rejecting any resume attempts while the route remains blocked.
4. **Interactive Teleoperation Menu (`turtle_menu.py`)**: Terminal menu to drive the turtle in custom patterns (Patrol, Rectangle, Zigzag).
5. **Telemetry Publisher & Monitor**: Publishes simulated rover metrics and flags warnings if battery levels drop below threshold levels.

---

## 📂 Repository Structure

```text
whatever_rover/
├── .gitignore
├── README.md
└── src/
    └── rover_telemetry/
        ├── package.xml
        ├── setup.py
        ├── setup.cfg
        ├── resource/
        │   └── rover_telemetry
        ├── launch/
        │   └── waypoint_launch.py
        └── rover_telemetry/
            ├── __init__.py
            ├── telemetry_publisher.py
            ├── telemetry_monitor.py
            ├── state_machine.py
            ├── turtle_menu.py
            └── waypoint_navigator.py
🛠️ Dependencies Installation
Make sure your ROS 2 desktop environment and turtlesim package are installed[cite: 13]:

Bash
sudo apt update
sudo apt install ros-jazzy-turtlesim
⚙️ Build Commands
[cite: 13]
Navigate to your workspace root directory:
Bash
cd ~/altair_phase3_ws/whatever_rover


Build the package using colcon:
Bash
colcon build --packages-select rover_telemetry


Source your workspace environment:
Bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash


Run Commands
1. Launch Autonomous Waypoint Navigation
To start both the Turtlesim simulator and the waypoint navigation node together with a single command:
Bash
ros2 launch rover_telemetry waypoint_launch.py
Mission Route: The rover navigates autonomously from start to Bottle (8.0, 5.5), then Mallet (8.0, 8.0), and finally Base (5.5, 5.5), finishing with a DONE announcement.


2. Testing Safety Interruption & Resume Control
While the rover is navigating between waypoints, test the blockage and service resume logic across separate terminals:

Trigger a Route Blockage (Pause):
Bash
ros2 topic pub /field_blocked std_msgs/msg/Bool "{data: true}" -1
(The rover halts immediately and holds zero velocity).


Try to Resume While Blocked (Should Reject):
Bash
ros2 service call /resume_mission std_srvs/srv/Trigger


Clear the Blockage Report:
Bash
ros2 topic pub /field_blocked std_msgs/msg/Bool "{data: false}" -1
(Notice the rover remains stationary, verifying no automatic resumption occurs).

Explicitly Resume Mission via Service:

Bash
ros2 service call /resume_mission std_srvs/srv/Trigger
(The rover resumes its journey to the remaining targets).

🕹️ Additional Executables
Interactive Teleop Menu:

Bash
ros2 run rover_telemetry turtle_menu
Telemetry Publisher:

Bash
ros2 run rover_telemetry telemetry_publisher
Telemetry Monitor:

Bash
ros2 run rover_telemetry telemetry_monitor
