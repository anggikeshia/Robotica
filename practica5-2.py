#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
PI = 3.1415926535897

range_rear = 0
range_left = 0
range_right = 0

def callback(data):
    global range_rear
    global range_left
    global range_right
    range_rear = data.range
    range_left = data.range
    range_right = data.range
    #print ("range rear", range_rear)
    print ("range left", range_left)
    #print ("range right", range_right)


def move():
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)
    range_rear_sub = rospy.Subscriber('/komodo_1/Rangers/Rear_URF', Range,callback)
    range_left_sub = rospy.Subscriber('/komodo_1/Rangers/Left_URF', Range,callback)
    range_right_sub = rospy.Subscriber('/komodo_1/Rangers/Right_URF', Range,callback)
    vel_msg = Twist()
    
    speed = 2
    angle = 120
    #clockwise = 1 #True or false

    #Converting from angles to radians
    angular_speed = speed*2*PI/360

    global range_rear
    global range_left
    global range_right
    while not rospy.is_shutdown():
        if (range_left > 0.7):
            #print ("rangeeeee", range_left)
            velocity_publisher.publish(vel_msg)
            vel_msg.angular.z = -abs(angular_speed) 
        else:
            if (range_rear > 0.7):
                #print ("rangeeeee", range_rear)
                velocity_publisher.publish(vel_msg)
                vel_msg.linear.x = -abs(speed)  
            else: 
                if (range_right > 0.7):
                    #print ("rangeeeee", range_right)
                    velocity_publisher.publish(vel_msg)
                    vel_msg.angular.z = abs(angular_speed)  
                else: 
                    vel_msg.linear.x = 0 
                    velocity_publisher.publish(vel_msg) 
    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass