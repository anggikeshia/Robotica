!#/usr/bin/env python
import roslib; roslib.load_manifest('rviz')
import rospy
from sensor_msgs.msg import Range

def talker():
    pub = rospy.Publisher('range', Range)
    rospy.init_node('talker')
    ranges = [float('NaN'), 1.0, -float('Inf'), 3.0, float('Inf')]
    min_range = 2.0
    max_range = 2.0
    while not rospy.is_shutdown():
        for rg in ranges:
            r = Range()
            r.header.stamp = rospy.Time.now()
            r.header.frame_id = "/base_link"
            r.radiation_type = 0
            r.field_of_view = 0.1
            r.min_range = min_range
            r.max_range = max_range
            r.range = rg
            pub.publish(r)
            rospy.sleep(1.0)
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass