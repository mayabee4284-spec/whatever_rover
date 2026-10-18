import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RoverStateMachine(Node):
    def __init__(self):
        super().__init__('rover_state_machine')
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.run_state_machine)
        
        # States: INIT -> STOP_1 -> STOP_2 -> STOP_3 -> COMPLETE
        self.states = ['INIT', 'NAVIGATING_STOP_1', 'STOP_1', 'NAVIGATING_STOP_2', 'STOP_2', 'NAVIGATING_STOP_3', 'STOP_3', 'COMPLETE']
        self.current_state_idx = 0
        self.interrupt_triggered = False
        
        self.get_logger().info('State Machine initialized at INIT state')

    def publish_stop(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

    def publish_move(self):
        twist = Twist()
        twist.linear.x = 0.5  # Moving forward at 0.5 m/s
        twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

    def run_state_machine(self):
        if self.interrupt_triggered:
            self.get_logger().warn('INTERRUPT DETECTED! Halting rover for safety...')
            self.publish_stop()
            return

        current_state = self.states[self.current_state_idx]
        self.get_logger().info(f'Current State: [{current_state}]')

        if 'NAVIGATING' in current_state:
            self.publish_move()
            self.get_logger().info('Moving towards target waypoint...')
            time.sleep(2)  # Simulate travel time
            self.current_state_idx += 1
            
        elif 'STOP' in current_state:
            self.publish_stop()
            self.get_logger().info(f'Reached {current_state}. Pausing for inspection...')
            time.sleep(3)  # Stop for 3 seconds
            self.current_state_idx += 1

        elif current_state == 'INIT':
            self.current_state_idx += 1

        elif current_state == 'COMPLETE':
            self.publish_stop()
            self.get_logger().info('Mission Complete! All 3 stops successfully reached.')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = RoverStateMachine()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()