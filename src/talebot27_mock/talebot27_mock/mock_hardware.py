import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Quaternion
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan

class MockHardware(Node):
    def __init__(self):
        super().__init__('talebot27_mock_hardware')
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_cb, 10)
        self.odom_pub = self.create_publisher(Odometry, '/wheel/odom', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.scan_pub = self.create_publisher(LaserScan, '/scan', 10)

        self.x, self.y, self.yaw = 0.35, 0.35, 0.0
        self.vx, self.wz = 0.0, 0.0
        self.dt = 0.05
        self.timer = self.create_timer(self.dt, self.loop)

    def cmd_cb(self, msg):
        self.vx = msg.linear.x
        self.wz = msg.angular.z

    def loop(self):
        now = self.get_clock().now().to_msg()
        self.yaw += self.wz * self.dt
        self.x += self.vx * math.cos(self.yaw) * self.dt
        self.y += self.vx * math.sin(self.yaw) * self.dt

        qz = math.sin(self.yaw / 2.0)
        qw = math.cos(self.yaw / 2.0)

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation = Quaternion(x=0.0, y=0.0, z=qz, w=qw)
        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.angular.z = self.wz
        self.odom_pub.publish(odom)

        imu = Imu()
        imu.header.stamp = now
        imu.header.frame_id = 'imu_frame'
        imu.angular_velocity.z = self.wz
        imu.orientation = Quaternion(x=0.0, y=0.0, z=qz, w=qw)
        self.imu_pub.publish(imu)

        scan = LaserScan()
        scan.header.stamp = now
        scan.header.frame_id = 'laser_frame'
        scan.angle_min, scan.angle_max = -math.pi, math.pi
        scan.angle_increment = math.pi / 90.0
        scan.range_min, scan.range_max = 0.05, 4.0
        
        ranges = []
        angle = scan.angle_min
        while angle <= scan.angle_max:
            ray = self.yaw + angle
            dx = (3.0 - self.x)/math.cos(ray) if math.cos(ray) > 1e-3 else ((-self.x)/math.cos(ray) if math.cos(ray) < -1e-3 else 5.0)
            dy = (2.0 - self.y)/math.sin(ray) if math.sin(ray) > 1e-3 else ((-self.y)/math.sin(ray) if math.sin(ray) < -1e-3 else 5.0)
            val = [d for d in [dx, dy] if d > 0]
            ranges.append(min(min(val) if val else 3.5, 3.5))
            angle += scan.angle_increment
        scan.ranges = ranges
        self.scan_pub.publish(scan)

def main():
    rclpy.init()
    node = MockHardware()
    rclpy.spin(node)
    rclpy.shutdown()
