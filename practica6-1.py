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
		distancia_actual = range_urf
		distancia_deseada = 0.7
		error = distancia_deseada - distancia_actual
		#si kp > mas rapido si kp < mas lento
		if (distancia_actual < distancia_deseada):
			kp = 1
			variacion = kp * error
			#print ("da", distancia_actual)
			#print ("variacion", variacion)
			velocity_publisher.publish(vel_msg)
			vel_msg.linear.x = -abs(variacion)  
		else: 
			if (distancia_actual > distancia_deseada):
				kp = 2
				variacion = kp * error
				#print ("rangeeeee", range_urf)
				velocity_publisher.publish(vel_msg)
				vel_msg.linear.x = -abs(variacion)
			else:
				if (distancia_actual == 0.2):
					vel_msg.linear.x = 0 
					velocity_publisher.publish(vel_msg) 
    rospy.spin()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass