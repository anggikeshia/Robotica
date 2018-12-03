#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
PI = 3.1415926535897

range_left = 0

def callback(data):
    global range_left
    range_left = data.range
  
def move():
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)
    #velocity_publisher = rospy.Publisher('/komodo_1/cmd_vel', Twist, queue_size=10)
    range_left_sub = rospy.Subscriber('/komodo_1/Rangers/Left_URF', Range,callback)
    vel_msg = Twist()
    rate = rospy.Rate(10)

    '''wheel_base_lenght=0.396
                wheel_diameter=0.2622
                encoder_cpr=2048'''
    radio = 0.46
    distancia = 2 * PI * radio
    distancia_deseada = 0.10
    speed=30
    lasterror=0
    while not rospy.is_shutdown():
        for i in range (5):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            vel_msg.angular.z= speed * 2 * PI / (360)
            vel_msg.linear.x = radio * speed * 2 * PI / (360)
            distancia_actual_left = range_left
            #control pid
            error2 = distancia_deseada - distancia_actual_left
            if distancia_actual_left > 0.4 and distancia_actual_left < 0.8:
                print ("angela", vel_msg.linear.x)
                kp=7
                kd=10
                variacion = kp * error2 + kd*(error2-lasterror)
                vel_msg.angular.z = vel_msg.angular.z + variacion
            lasterror=error2
        rate.sleep()
    rospy.spin()


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass