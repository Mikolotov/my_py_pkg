#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed


class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery_node")
        self.battery_state_ = "full"
        self.declare_parameter("battery_name", "Battery")
        self.battery_name_ = self.get_parameter("battery_name").get_parameter_value().string_value

        # Timer for battery state changes (1 second intervals)
        self.battery_timer_ = self.create_timer(1.0, self.update_battery_state)
        self.time_counter_ = 0
        
        self.get_logger().info("Battery Node started")

    def update_battery_state(self):
        self.time_counter_ += 1
        
        if self.battery_state_ == "full" and self.time_counter_ >= 4:
            self.battery_state_ = "empty"
            self.time_counter_ = 0
            self.get_logger().info(f"🔋 {self.battery_name_} is now EMPTY!")
            self.call_led_service(-1, "on")
            
        elif self.battery_state_ == "empty" and self.time_counter_ >= 6:
            self.battery_state_ = "full"
            self.time_counter_ = 0
            self.get_logger().info(f"🔋 {self.battery_name_} is now FULL!")
            self.call_led_service(-2, "off")

    def call_led_service(self, led_number, state):
        client = self.create_client(SetLed, "set_led")
        if not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("LED service not available")
            return

        request = SetLed.Request()
        request.led_number = led_number
        request.state = state
        client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()