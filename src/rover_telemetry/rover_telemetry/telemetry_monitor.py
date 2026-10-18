import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TelemetryMonitor(Node):
    def __init__(self):
        super().__init__('telemetry_monitor')
        self.subscription = self.create_subscription(
            String,
            'rover_status',
            self.listener_callback,
            10)
        self.get_logger().info('Rover Telemetry Monitor (Mission Control) Started')

    def listener_callback(self, msg):
        # Print the incoming telemetry packet normally
        self.get_logger().info(f'Received Telemetry: "{msg.data}"')
        
        # Parse the battery level from the string to check the 25% threshold rule
        try:
            if "BATTERY:" in msg.data:
                # Extract the numeric value after "BATTERY:"
                parts = msg.data.split('|')[0]  # e.g., "BATTERY: 24.0% "
                battery_str = parts.split(':')[1].replace('%', '').strip()
                battery_val = float(battery_str)
                
                # Check safety warning requirement (< 25%)
                if battery_val < 25.0:
                    self.get_logger().warn(
                        f'⚠️ LOW BATTERY WARNING! Power is at {battery_val}% — Below 25% threshold!'
                    )
        except Exception as e:
            # Fallback if parsing encounters any unexpected formatting
            pass

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()