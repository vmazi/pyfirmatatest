import pyfirmata

import pygame
import keyboard

DEADZONE = .2

pygame.init()
joysticks = []
clock = pygame.time.Clock()

MIN_ANGLE = 10

MAX_ANGLE_FULL = 180

MAX_ANGLE_HALF = 110

# set up arduino board
board = pyfirmata.Arduino('COM3')

# # %% setup servo on pin 2
# angle_servo1 = 10  # initial angle
da = .25  # initial speed (degrees per keypress)


# servo1 = board.get_pin('d:2:s')  # pin to communicate to the servo with
# servo1.write(angle_servo1)  # set servo to initial angle
#
# angle_servo2 = 10  # initial angle
# servo2 = board.get_pin('d:3:s')  # pin to communicate to the servo with
# servo2.write(angle_servo2)  # set servo to initial angle

class Servo:
    def __init__(self, angle_servo, pin):
        self.angle_servo = angle_servo
        self.servo = board.get_pin('d:' + str(pin) + ':s')


servo_init_angle = [50, 33, 47, 130, 90, 104, 50, 33, 47, 80, 90, 87]

servomotors = []
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
    print("Detected joystick " + joysticks[-1].get_name() + "'")


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


events = []
# %% while loop
gpad = joysticks[-1]


def decrease_servo_angle(servo_num, min_angle):
    servomotors[servo_num].angle_servo = dec_serv_angle(servomotors[servo_num].angle_servo, da, min_angle,
                                                        servomotors[servo_num].servo)


def increase_servo_angle(servo_num, max_angle):
    servomotors[servo_num].angle_servo = inc_serv_angle(servomotors[servo_num].angle_servo, da, max_angle,
                                                        servomotors[servo_num].servo)


def check_claw_input():
    if gpad.get_button(pygame.CONTROLLER_BUTTON_A):
        increase_servo_angle(0, 88)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_B):
        decrease_servo_angle(0, 40)


def check_silver_claw_input():
    if gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) > .5:
        increase_servo_angle(6, 88)
    elif gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) > .5:
        decrease_servo_angle(6, 40)


def check_claw_rotate():
    if gpad.get_button(pygame.CONTROLLER_BUTTON_X):
        decrease_servo_angle(1, MIN_ANGLE)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_Y):
        increase_servo_angle(1, MAX_ANGLE_FULL)


def check_silver_claw_rotate():
    if gpad.get_button(4):
        decrease_servo_angle(7, MIN_ANGLE)
    elif gpad.get_button(5):
        increase_servo_angle(7, MAX_ANGLE_FULL)


def check_tert_vert():
    if check_stick_left(horizontal_axis_l, vertical_axis_l):
        decrease_servo_angle(2, MIN_ANGLE)
    elif check_stick_right(horizontal_axis_l, vertical_axis_l):
        increase_servo_angle(2, MAX_ANGLE_FULL)


def check_silver_tert_vert():
    if keyboard.is_pressed('h'):
        decrease_servo_angle(8, MIN_ANGLE)
    elif keyboard.is_pressed('j'):
        increase_servo_angle(8, MAX_ANGLE_FULL)


def check_secondary_vert():
    if check_stick_up(horizontal_axis_l, vertical_axis_l):
        decrease_servo_angle(3, MIN_ANGLE)
    elif check_stick_down(horizontal_axis_l, vertical_axis_l):
        increase_servo_angle(3, MAX_ANGLE_FULL)


def check_silver_secondary_vert():
    if keyboard.is_pressed('n'):
        decrease_servo_angle(9, MIN_ANGLE)
    elif keyboard.is_pressed('m'):
        increase_servo_angle(9, MAX_ANGLE_FULL)


def check_primary_vert():
    if check_stick_up(horizontal_axis_r, vertical_axis_r):
        decrease_servo_angle(4, MIN_ANGLE)
    elif check_stick_down(horizontal_axis_r, vertical_axis_r):
        increase_servo_angle(4, MAX_ANGLE_FULL)


def check_silver_primary_vert():
    if gpad.get_hat(0) == (0,-1):
        decrease_servo_angle(10, MIN_ANGLE)
    elif gpad.get_hat(0) == (0, 1):
        increase_servo_angle(10, MAX_ANGLE_FULL)


def check_base_rotate():
    if check_stick_left(horizontal_axis_r, vertical_axis_r):
        decrease_servo_angle(5, 36.5)
    elif check_stick_right(horizontal_axis_r, vertical_axis_r):
        increase_servo_angle(5, 167)


def check_silver_base_rotate():
    if gpad.get_hat(0) == (-1, 0):

        decrease_servo_angle(11, 36.5)
    elif gpad.get_hat(0) == (1, 0):
        increase_servo_angle(11, 167)


def check_move_to_stance():
    if keyboard.is_pressed('s'):
        servomotors[2].angle_servo = 42.5
        move_servo(servomotors[2].servo, servomotors[2].angle_servo)
        servomotors[4].angle_servo = 100.0
        move_servo(servomotors[4].servo, servomotors[4].angle_servo)


def check_chop_input():
    if keyboard.is_pressed('c'):
        servomotors[2].angle_servo = 35.0
        move_servo(servomotors[2].servo, servomotors[2].angle_servo)
        servomotors[4].angle_servo = 82.0
        move_servo(servomotors[4].servo, servomotors[4].angle_servo)


def check_print_angle():
    global i
    if keyboard.is_pressed('a'):
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT))
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT))
        for i in range(0, len(servomotors)):
            print('servo:' + str(i) + ' has angle: ', str(servomotors[i].angle_servo))


if __name__ == '__main__':
    while True:
        clock.tick(120)

        new_events = pygame.event.get()
        if len(new_events) != 0:
            events = new_events
            for event in events:
                print(event)

        horizontal_axis_l = gpad.get_axis(0)
        vertical_axis_l = gpad.get_axis(1)

        horizontal_axis_r = gpad.get_axis(2)
        vertical_axis_r = gpad.get_axis(3)

        check_claw_input()

        check_claw_rotate()

        check_tert_vert()

        check_secondary_vert()

        check_primary_vert()

        check_base_rotate()

        check_print_angle()

        check_move_to_stance()

        check_chop_input()

        check_silver_claw_input()

        check_silver_claw_rotate()

        check_silver_tert_vert()

        check_silver_secondary_vert()

        check_silver_primary_vert()

        check_silver_base_rotate()

        if gpad.get_button(9):
            print("right stick pressed")

        if gpad.get_button(8):
            print("left stick pressed")
