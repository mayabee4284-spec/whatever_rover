import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty

class TurtleMenuNode(Node):
    def __init__(self):
        super().__init__('turtle_menu_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('Turtle Driving Menu Node Initialized.')
        self.print_menu()

    def print_menu(self):
        print("\n=== TURTLE DRIVING MENU ===")
        print("P : Patrol (Drive forward, turn 180°, and return near start)")
        print("R : Rectangle (Trace a rectangle with two distinct side lengths)")
        print("Z : Zigzag (Drive three forward segments, alternating turns)")
        print("Q : Quit (Stop and exit)")
        print("===========================")
        print("Enter choice (P/R/Z/Q): ", end="", flush=True)

    def send_velocity(self, linear_x, angular_z, duration):
        """Helper to publish velocity for a specific duration (timed movement)"""
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        
        # Publish continuously for the given duration
        rate = 10  # 10 Hz
        num_iterations = int(duration * rate)
        for _ in range(num_iterations):
            if not rclpy.ok():
                break
            self.publisher_.publish(twist)
            rclpy.spin_once(self, timeout_sec=1.0 / rate)
            
        # Send a stop command after the movement
        self.stop_turtle()

    def stop_turtle(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.publisher_.publish(twist)

    def execute_pattern(self, choice):
        choice = choice.upper()
        if choice == 'P':
            self.get_logger().info('Executing Patrol: Driving forward, turning 180°, and returning...')
            # 1. Drive forward ~3 seconds
            self.send_velocity(2.0, 0.0, 3.0)
            # 2. Turn 180 degrees (~3.14 rads)
            self.send_velocity(0.0, 2.0, 1.57)
            # 3. Return near starting position
            self.send_velocity(2.0, 0.0, 3.0)
            self.get_logger().info('Patrol complete.')

        elif choice == 'R':
            self.get_logger().info('Executing Rectangle trace...')
            # Side 1 (Long)
            self.send_velocity(2.0, 0.0, 2.5)
            self.send_velocity(0.0, 1.57, 1.0) # Turn 90 deg
            # Side 2 (Short)
            self.send_velocity(2.0, 0.0, 1.5)
            self.send_velocity(0.0, 1.57, 1.0) # Turn 90 deg
            # Side 3 (Long)
            self.send_velocity(2.0, 0.0, 2.5)
            self.send_velocity(0.0, 1.57, 1.0) # Turn 90 deg
            # Side 4 (Short)
            self.send_velocity(2.0, 0.0, 1.5)
            self.send_velocity(0.0, 1.57, 1.0) # Turn 90 deg
            self.get_logger().info('Rectangle complete.')

        elif choice == 'Z':
            self.get_logger().info('Executing Zigzag...')
            # Segment 1
            self.send_velocity(2.0, 0.0, 2.0)
            self.send_velocity(0.0, 1.57, 0.8) # Left turn
            # Segment 2
            self.send_velocity(2.0, 0.0, 2.0)
            self.send_velocity(0.0, -1.57, 0.8) # Right turn
            # Segment 3
            self.send_velocity(2.0, 0.0, 2.0)
            self.get_logger().info('Zigzag complete.')

        elif choice == 'Q':
            self.get_logger().info('Quitting application. Sending stop command.')
            self.stop_turtle()
            return False
        else:
            self.get_logger().warn('Invalid input! Please press P, R, Z, or Q.')
            
        return True

def main(args=None):
    rclpy.init(args=args)
    node = TurtleMenuNode()
    
    # Simple non-blocking or line-based input loop for terminal selection
    try:
        while rclpy.ok():
            # Read single line from terminal safely
            choice = input()
            if choice:
                keep_running = node.execute_pattern(choice.strip())
                if not keep_running:
                    break
                node.print_menu()
    except KeyboardInterrupt:
        node.stop_turtle()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()