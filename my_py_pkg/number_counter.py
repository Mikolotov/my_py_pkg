#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
    
    
class NumberCounter(Node): 
    def __init__(self):
        super().__init__("number_counter") 
        self.counter_ = 0
        self.subscriber_ = self.create_subscription(
            Int64, "number",self.callback_number_publisher, 10)
        self.publisher_ = self.create_publisher(Int64, "number_counter", 10)
        self.timer_ = self.create_timer(0.5, self.publish_counter)
        self.get_logger().info("Number counter has been started")
    
    def callback_number_publisher(self, msg: Int64):
        self.get_logger().info(str(msg.data))
        self.counter_ += msg.data

    def publish_counter(self):
        msg = Int64()
        msg.data = self.counter_
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter() 
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()