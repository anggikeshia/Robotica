#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

range_urf = 0

def callback(data):
	global range_urf
	range_urf = data.range
	print ("rangeeeee", range_urf)
	#rospy.loginfo(range)
	#rospy.spin()

def move():
    rospy.init_node('robot_cleaner', anonymous=True)
    #velocity_publisher = rospy.Publisher('/komodo_1/cmd_vel', Twist, queue_size=10)
    velocity_publisher = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)
    range_urf_sub = rospy.Subscriber('/komodo_1/Rangers/Rear_URF/', Range, callback)
    vel_msg = Twist()
    speed = 0.1
    
    global range_urf

    while not rospy.is_shutdown():
        if (range_urf < 0.7):
            velocity_publisher.publish(vel_msg)
            vel_msg.linear.x = -abs(speed) 
            print ("speed", vel_msg.linear.x)
        else: 
            vel_msg.linear.x = 0 
            print ("speed", vel_msg.linear.x)
            velocity_publisher.publish(vel_msg) 
    
    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass