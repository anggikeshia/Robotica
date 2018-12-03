#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
PI = 3.1415926535897

range_rear = 0
range_left = 0

def callback(data):
    global range_rear
    global range_left
    range_rear = data.range
    range_left = data.range
    #print ("range rear", range_rear)
    #print ("range left", range_left)
   
def move():
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)
    range_rear_sub = rospy.Subscriber('/komodo_1/Rangers/Rear_URF', Range,callback)
    range_left_sub = rospy.Subscriber('/komodo_1/Rangers/Left_URF', Range,callback)
    vel_msg = Twist()
    
    speed = 2
    angle = 90
    #clockwise = 1 #True or false

    #Converting from angles to radians
    angular_speed = speed*2*PI/360
    global range_rear
    global range_left
    

    while not rospy.is_shutdown():
		distancia_deseada = 0.7
		distancia_actual_left = range_left
		distancia_actual_rear = range_rear
		error1 = distancia_deseada - distancia_actual_rear
		error2 = distancia_deseada - distancia_actual_left
		if (range_left == distancia_deseada and range_rear > distancia_deseada):
			kp = 2
			variacion = kp * error1
			#print ("rangeeeee", range_left)
			velocity_publisher.publish(vel_msg)
			vel_msg.linear.x = -abs(variacion)
		else:
			if (range_rear < distancia_deseada):
				#print ("rangeeeee", range_rear)
				velocity_publisher.publish(vel_msg)
				vel_msg.angular.z = -abs(angular_speed)  
			else: 
				vel_msg.linear.x = 0 
				velocity_publisher.publish(vel_msg) 
    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass