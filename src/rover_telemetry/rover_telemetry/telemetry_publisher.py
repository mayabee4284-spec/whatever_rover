import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TelemetryPublisher(Node):
    def __init__(self):
        super().__init__('telemetry_publisher')
        self.publisher_ = self.create_publisher(String, 'rover_status', 10)
        self.timer = self.create_timer(1.0, self.publish_telemetry)
        
        # Simulation variables
        self.battery_level = 50.0  
        self.temperature = 25.5    # Celsius
        self.wheel_speed = 1.2     # m/s
        self.elapsed_time = 0      # seconds

    def publish_telemetry(self):
        # Simulate changes every second
        if self.battery_level > 5.0:
            self.battery_level -= 1.5  # Deplete battery gradually
        self.temperature += 0.2        # Temperature rises slightly
        self.elapsed_time += 1         # Time ticks up

        # Format the telemetry message packet with explicit units
        msg_text = (
            f"BATTERY: {self.battery_level:.2f}% | "
            f"TEMP: {self.temperature:.1f}°C | "
            f"SPEED: {self.wheel_speed:.1f} m/s | "
            f"TIME: {self.elapsed_time}s"
        )

        msg = String()
        msg.data = msg_text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()