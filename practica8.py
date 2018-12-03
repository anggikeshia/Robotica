#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
import numpy as np

range_rear = 0
range_left = 0
range_right = 0

def callback(data):
    global range_rear
    global range_left
    global range_right
    #print "Left" in data.header.frame_id, data.header.frame_id
    #print type(data)
    range_rear = data.range if "Rear" in data.header.frame_id else -1
    range_left = data.range if "Left" in data.header.frame_id else -1
    range_right = data.range if "Right" in data.header.frame_id else -1
    #print ("range rear", range_rear)
    #print ("range left", range_left)
    #print ("range right", range_right)


	#Dimensiones del mapa
alto = 10
ancho = 10

matriz_ocupacion = np.zeros((alto,ancho))


def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)
    range_rear_sub = rospy.Subscriber('/komodo_1/Rangers/Rear_URF', Range,callback)
    range_left_sub = rospy.Subscriber('/komodo_1/Rangers/Left_URF', Range,callback)
    range_right_sub = rospy.Subscriber('/komodo_1/Rangers/Right_URF', Range,callback)
    vel_msg = Twist()
    
    #Receiveing the user's input
    print("Moviendo mi robot")
    speed = 1
    distance = 5
    isForward = 1
    ini_f = 4
    ini_c = 4

    global range_rear
    global range_left
    global range_right
    rate = rospy.Rate(5)
    
    #revisa si va adelante o hacia atras
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    
    while not rospy.is_shutdown():
        #Setting the current time for distance calculus
        t0 = float(rospy.Time.now().to_sec())
        current_distance = 0
        while(current_distance < distance):
            cont = 0 
            cont1 = 0
            cont2 = 0 
        	#print ("range right", range_right)
            if (range_right > 0.1 and range_right < 1.0):
				cont = cont + 1 
				if cont >= 1:
					matriz_ocupacion [ini_f + current_distance][ini_c+2] = 1   #2,3 111,111
					#print matriz_ocupacion
					print "ja"
            if (range_left > 0.1 and range_left < 1.0):
				cont1 = cont1 + 1 
				if cont1 >= 1:
					matriz_ocupacion [ini_f + current_distance][ini_c - 2] = 1   #2,3 111,111
					#print matriz_ocupacion
					print "je"
            if (range_rear > 0.1 and range_rear < 1.0):
				cont2 = cont2 + 1 
				if cont2 >= 1:
					matriz_ocupacion [ini_f][ini_c] = 1   #2,3 111,111
					#print matriz_ocupacion
					print "ji"
            print matriz_ocupacion
            print '\n \n'
            velocity_publisher.publish(vel_msg) 
            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
            current_distance = int(speed*(t1-t0))
            #print ("jaja",current_distance)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        exit()
