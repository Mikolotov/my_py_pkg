#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
    
    
class RobotNewsStationNode(Node):
    def __init__(self):
        super().__init__("robot_news_station")
        self.declare_parameter("robot_name", "C3PO")
        self.robot_name_ = self.get_parameter("robot_name").get_parameter_value().string_value
        self.declare_parameter("timer_interval", 1.0)
        self.timer_interval_ = self.get_parameter("timer_interval").get_parameter_value().double_value

        
        self.publishers_ =self.create_publisher(String, "robot_news", 10)
        self.timer_ = self.create_timer(self.timer_interval_, self.publish_news)
        self.get_logger().info("Robot News Station has been started.")

    def publish_news(self): 
        msg = String()
        msg.data = "Hi, this is " + self.robot_name_ + " from the robot news station."
        self.publishers_.publish(msg)
        #self.get_logger().info(f"Published: {msg.data}")
    
def main(args=None):
    rclpy.init(args=args)
    node = RobotNewsStationNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()