from time import sleep

import pyfirmata

import pygame
import keyboard

DEADZONE = .2

MIN_ANGLE = 10

MAX_ANGLE_FULL = 180

MAX_ANGLE_HALF = 110

# set up arduino board
board = pyfirmata.Arduino('COM3')

# # %% setup servo on pin 2
# angle_servo1 = 10  # initial angle
da = .5  # initial speed (degrees per keypress)


class Servo:
    def __init__(self, angle_servo, pin):
        self.angle_servo = angle_servo
        self.servo = board.get_pin('d:' + str(pin) + ':s')


servo_init_angle = [50, 33, 47, 130, 90, 104, 50, 33, 47, 80, 90, 87]

servomotors = []


def setup_arm_control():
    pygame.init()
    joysticks = []

    for i in range(2, 14):
        servo_motor = Servo(servo_init_angle[i - 2], i)
        servo_motor.servo.write(servo_motor.angle_servo)
        servomotors.append(servo_motor)
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create a Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize the appended joystick (-1 means last array item)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print('Detected joystick ' + joysticks[-1].get_name() + '')
    return joysticks


# set up a function that will tell the servo to move to a specific position when called
def move_servo(servo, deg):  # define function
    servo.write(deg)  # move servo to specified angle


def check_stick_up(x_axis, y_axis):
    return y_axis < -DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_down(x_axis, y_axis):
    return y_axis > DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_left(x_axis, y_axis):
    return x_axis < -DEADZONE and abs(x_axis) > abs(y_axis)


def check_stick_right(x_axis, y_axis):
    return x_axis > DEADZONE and abs(x_axis) > abs(y_axis)


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


def decrease_servo_angle(servo_num, min_angle):
    servomotors[servo_num].angle_servo = dec_serv_angle(servomotors[servo_num].angle_servo, da, min_angle,
                                                        servomotors[servo_num].servo)


def increase_servo_angle(servo_num, max_angle):
    servomotors[servo_num].angle_servo = inc_serv_angle(servomotors[servo_num].angle_servo, da, max_angle,
                                                        servomotors[servo_num].servo)


def check_silver_claw_rotate():
    if keyboard.is_pressed('n'):
        increase_servo_angle(7, MAX_ANGLE_FULL)
    elif keyboard.is_pressed('m'):
        decrease_servo_angle(7, MIN_ANGLE)


def check_silver_claw_grab():
    if keyboard.is_pressed('h'):
        increase_servo_angle(6, 88)
    elif keyboard.is_pressed('j'):
        decrease_servo_angle(6, 40)


def check_silver_tert_vert(gpad):
    if gpad.get_button(4):
        decrease_servo_angle(8, MIN_ANGLE)
    elif gpad.get_button(5):
        increase_servo_angle(8, MAX_ANGLE_FULL)


def check_silver_secondary_vert(gpad):
    if gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) > .5:
        decrease_servo_angle(9, MIN_ANGLE)
    elif gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) > .5:
        increase_servo_angle(9, MAX_ANGLE_FULL)


def check_silver_primary_vert(gpad):
    if gpad.get_hat(0) == (0, -1):
        increase_servo_angle(10, MAX_ANGLE_FULL)
    elif gpad.get_hat(0) == (0, 1):
        decrease_servo_angle(10, MIN_ANGLE)


def check_silver_base_rotate(gpad):
    if gpad.get_hat(0) == (-1, 0):
        increase_servo_angle(11, 167)
    elif gpad.get_hat(0) == (1, 0):
        decrease_servo_angle(11, 36.5)


def check_claw_rotate(gpad):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_X):
        decrease_servo_angle(1, MIN_ANGLE)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_Y):
        increase_servo_angle(1, MAX_ANGLE_FULL)


def check_claw_grab(gpad):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_A):
        increase_servo_angle(0, 88)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_B):
        decrease_servo_angle(0, 40)


def check_tert_vert():
    if check_stick_left(horizontal_axis_l, vertical_axis_l):
        decrease_servo_angle(2, MIN_ANGLE)
    elif check_stick_right(horizontal_axis_l, vertical_axis_l):
        increase_servo_angle(2, MAX_ANGLE_FULL)


def check_secondary_vert():
    if check_stick_up(horizontal_axis_l, vertical_axis_l):
        increase_servo_angle(3, MAX_ANGLE_FULL)
    elif check_stick_down(horizontal_axis_l, vertical_axis_l):
        decrease_servo_angle(3, MIN_ANGLE)


def check_primary_vert():
    if check_stick_down(horizontal_axis_r, vertical_axis_r):
        increase_servo_angle(4, MAX_ANGLE_FULL)
    elif check_stick_up(horizontal_axis_r, vertical_axis_r):
        decrease_servo_angle(4, MIN_ANGLE)


def check_base_rotate():
    if check_stick_left(horizontal_axis_r, vertical_axis_r):
        increase_servo_angle(5, 167)
    elif check_stick_right(horizontal_axis_r, vertical_axis_r):
        decrease_servo_angle(5, 36.5)


def check_move_to_stance():
    if keyboard.is_pressed('s'):
        hold_pose = [{'ind': 6, 'angle': 40.5},
                     {'ind': 7, 'angle': 124.5},
                     {'ind': 8, 'angle': 141.5},
                     {'ind': 9, 'angle': 101.0},
                     {'ind': 10, 'angle': 107.5},
                     {'ind': 11, 'lag': .5, 'angle': 118.0}]
        move_arm_to_pos(hold_pose)


def check_move_to_init(gpad):
    if gpad.get_button(7):
        hold_pose = [{'ind': 5, 'angle': 104},
                     {'ind': 0, 'angle': 50},
                     {'ind': 1, 'angle': 33},
                     {'ind': 2, 'angle': 47},
                     {'ind': 3, 'angle': 130},
                     {'ind': 4, 'angle': 90}]
        move_arm_to_pos(hold_pose)
        hold_pose = [{'ind': 11, 'angle': 87},
                     {'ind': 6, 'angle': 50},
                     {'ind': 7, 'angle': 33},
                     {'ind': 8, 'angle': 47},
                     {'ind': 9, 'angle': 80},
                     {'ind': 10, 'angle': 90}]
        move_arm_to_pos(hold_pose)


def move_arm_to_pos(desired_pose):
    for increment in range(6):
        if 'lag' in desired_pose[increment]:
            sleep(desired_pose[increment].get('lag'))

        move_servo_to_angle(desired_pose[increment].get('ind'), desired_pose[increment].get('angle'))


def move_servo_to_angle(servo_ind, angle_to_set):
    servomotors[servo_ind].angle_servo = angle_to_set
    move_servo(servomotors[servo_ind].servo, servomotors[servo_ind].angle_servo)


def check_chop_input():
    if keyboard.is_pressed('c'):
        servomotors[2].angle_servo = 35.0
        move_servo(servomotors[2].servo, servomotors[2].angle_servo)
        servomotors[4].angle_servo = 82.0
        move_servo(servomotors[4].servo, servomotors[4].angle_servo)


def check_print_angle(gpad):
    if keyboard.is_pressed('p'):
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT))
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT))
        for index in range(0, len(servomotors)):
            print('servo:' + str(index) + ' has angle: ', str(servomotors[index].angle_servo))


def check_move_to_tool_select(gpad):
    if gpad.get_button(8):
        tool_grab_pose = [{'ind': 6, 'angle': 40.5},
                          {'ind': 7, 'angle': 124.5},
                          {'ind': 8, 'angle': 141.5},
                          {'ind': 9, 'angle': 101.0},
                          {'ind': 10, 'angle': 107.5},
                          {'ind': 11, 'lag': .5, 'angle': 118.0}]
        move_arm_to_pos(tool_grab_pose)


if __name__ == '__main__':

    joysticks = setup_arm_control()
    events = []
    # %% while loop
    gamepad = joysticks[-1]

    clock = pygame.time.Clock()

    while True:
        clock.tick(120)

        new_events = pygame.event.get()
        if len(new_events) != 0:
            events = new_events
            for event in events:
                print(event)

        horizontal_axis_l = gamepad.get_axis(0)
        vertical_axis_l = gamepad.get_axis(1)

        horizontal_axis_r = gamepad.get_axis(2)
        vertical_axis_r = gamepad.get_axis(3)

        check_claw_grab(gamepad)

        check_claw_rotate(gamepad)

        check_tert_vert()

        check_secondary_vert()

        check_primary_vert()

        check_base_rotate()

        check_print_angle(gamepad)

        check_move_to_stance()

        check_move_to_init(gamepad)
        #
        # check_chop_input()

        check_silver_claw_grab()

        check_silver_claw_rotate()

        check_silver_tert_vert(gamepad)

        check_silver_secondary_vert(gamepad)

        check_silver_primary_vert(gamepad)

        check_silver_base_rotate(gamepad)

        if gamepad.get_button(9):
            print('right stick pressed')

        check_move_to_tool_select(gamepad)
