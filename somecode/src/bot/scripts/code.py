import rospy
import sys
from gazebo_msgs.srv import ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3
from gazebo_msgs.srv import ApplyJointEffort

if __name__ == '__main__':
    rospy.init_node('Control')
    
    try:
        rospy.wait_for_service('/gazebo/apply_body_wrench', timeout=10)
    except rospy.ROSException:
        print('Service not available! Closing node...')
        sys.exit(-1)

    try:
        apply_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', ApplyBodyWrench)
    except rospy.ServiceException as e:
        print('Service call failed, error=', e)
        sys.exit(-1)

    try:
        apply_effort = rospy.ServiceProxy('/gazebo/apply_joint_effort', ApplyJointEffort)
    except rospy.ServiceException:
        sys.exit(-1)

    success = apply_effort(
            'r2/right_arm/joint1',
            100,
            rospy.Time().now(),
            rospy.Duration(10)
            )
    print(success)
    
    '''wrench = Wrench()
    wrench.force = Vector3(*force)
    wrench.torque = Vector3(*torque)
    success = apply_wrench(
        'youbot::arm_link_2',
        'world',
        Point(0, 0, 0),
        wrench,
        rospy.Time().now(),
        rospy.Duration(duration))

    if success:
        print('Body wrench perturbation applied!')
        print('\tDuration [s]: ', duration)
        print('\tForce [N]: ', force)
        print('\tTorque [Nm]: ', torque)
    else:
        print('Failed!')'''
