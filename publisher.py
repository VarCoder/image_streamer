import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image #### custom message
from cv_bridge import CvBridge
import cv2
import numpy as np
import os
class publisher(Node):
	def __init__(self):
		super().__init__('publisher')

		self.publisher_ = self.create_publisher(Image, 'Image', 10)
		timer_period = 0.5  # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.i = 0
		self.bridge = CvBridge()

		self.im_list = os.listdir("/home/shimizu/ros2_ws/src/qt_plugins/image_streamer/pizza_images")
		self.im_list = [self.bridge_img(f"/home/shimizu/ros2_ws/src/qt_plugins/image_streamer/pizza_images/{x}") for x in self.im_list]

		print(os.curdir)
		
	def bridge_img(self, img):
		np_img = cv2.imread(img)
		return self.bridge.cv2_to_imgmsg(np_img,encoding="bgr8")
	
	def timer_callback(self):
		self.cv_image = self.im_list[self.i]
		# self.cv_image = self.im_list[self.i] ### an RGB image
		# print(self.cv_image)

		self.publisher_.publish(self.cv_image)
		self.get_logger().info('Publishing an image')
		self.i = (self.i + 1) % len(self.im_list)
def main(args=None):
    rclpy.init(args=args)
    pub = publisher()
    rclpy.spin(pub)
    pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
   main()
