import time


# set up a function that will tell the servo to move to a specific position when called
def move_servo(servo, deg):  # define function
    servo.write(deg)  # move servo to specified angle


def inc_serv_angle(angle_servo, inc, max_ang, servo):
    if angle_servo + inc < max_ang:
        new_angle_servo = angle_servo + inc
        move_servo(servo, new_angle_servo)
        return new_angle_servo
    return angle_servo


def dec_serv_angle(angle_servo, inc, min_ang, servo):
    if angle_servo - inc > min_ang:
        new_angle_servo = angle_servo - inc
        move_servo(servo, new_angle_servo)
        return new_angle_servo
    return angle_servo


def move_arm_to_pos(desired_pose, servomotors):
    for increment in range(6):
        if 'lag' in desired_pose[increment]:
            time.sleep(desired_pose[increment].get('lag'))

        move_servo_to_angle(desired_pose[increment].get('ind'), desired_pose[increment].get('angle'), servomotors)


def move_servo_to_angle(servo_ind, angle_to_set, servomotors):
    servomotors[servo_ind].angle_servo = angle_to_set
    move_servo(servomotors[servo_ind].servo, servomotors[servo_ind].angle_servo)


def decrease_servo_angle(servo_num, min_angle, servomotors, degree_increment):
    servomotors[servo_num].angle_servo = dec_serv_angle(servomotors[servo_num].angle_servo, degree_increment, min_angle,
                                                        servomotors[servo_num].servo)


def increase_servo_angle(servo_num, max_angle, servomotors, degree_increment):
    servomotors[servo_num].angle_servo = inc_serv_angle(servomotors[servo_num].angle_servo, degree_increment, max_angle,
                                                        servomotors[servo_num].servo)
