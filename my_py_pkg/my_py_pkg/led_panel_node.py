#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from my_robot_interfaces.msg import LedPanelStatus


class LedPanelNode(Node):
    def __init__(self):
        super().__init__("led_panel_node")
        self.declare_parameter("led_states", [0, 0, 0])
        self.led_states_ = list(self.get_parameter("led_states").get_parameter_value().integer_array_value)

        self.server_ = self.create_service(SetLed, "set_led", self.set_led_callback)
        self.status_publisher_ = self.create_publisher(LedPanelStatus, "led_panel_status", 10)
        self.get_logger().info("LED Panel started")

    def publish_status(self):
        msg = LedPanelStatus()
        msg.led_states = self.led_states_
        self.status_publisher_.publish(msg)

    def set_led_callback(self, request, response):
        led_number = request.led_number

        if led_number == -1:  # Turn on next available LED
            return self.turn_on_next_led(response)
        elif led_number == -2:  # Turn off rightmost LED
            return self.turn_off_rightmost_led(response)
        else:
            response.success = False
            return response

    def turn_on_next_led(self, response):
        for i in range(len(self.led_states_)):
            if self.led_states_[i] == 0:
                self.led_states_[i] = 1
                response.success = True
                response.message = f"LED {i} turned on"
                self.publish_status()
                return response
        
        response.success = False
        response.message = "All LEDs already on"
        return response

    def turn_off_rightmost_led(self, response):
        for i in range(len(self.led_states_) - 1, -1, -1):
            if self.led_states_[i] == 1:
                self.led_states_[i] = 0
                response.success = True
                response.message = f"LED {i} turned off"
                self.publish_status()
                return response
        
        response.success = False
        response.message = "All LEDs already off"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()