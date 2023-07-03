# %% import libraries
import time
import keyboard
import pyfirmata

import pygame

DEADZONE = .2

pygame.init()
joysticks = []
clock = pygame.time.Clock()

MIN_ANGLE = 10

MAX_ANGLE_FULL = 180

MAX_ANGLE_HALF = 90

# set up arduino board
board = pyfirmata.Arduino('COM4')

# %% setup servo on pin 2
angle_servo1 = 10  # initial angle
da = 2  # initial speed (degrees per keypress)
servo1 = board.get_pin('d:2:s')  # pin to communicate to the servo with
servo1.write(angle_servo1)  # set servo to initial angle

# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize the appended joystick (-1 means last array item)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print("Detected joystick " + joysticks[-1].get_name() + "'")


# set up a function that will tell the servo to move to a specific position when called
def move_servo(servo, deg):  # define function
    servo.write(deg)  # move servo to specified angle


# %%
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
while True:
    clock.tick(60)

    new_events = pygame.event.get()
    if len(new_events) != 0:
        events = new_events

    horizontal_axis_l = joysticks[-1].get_axis(0)
    vertical_axis_l = joysticks[-1].get_axis(1)

    horizontal_axis_r = joysticks[-1].get_axis(2)
    vertical_axis_r = joysticks[-1].get_axis(3)

    if joysticks[-1].get_button(pygame.CONTROLLER_BUTTON_A):
        angle_servo1 = dec_serv_angle(angle_servo1, da, MIN_ANGLE, servo1)

    elif joysticks[-1].get_button(pygame.CONTROLLER_BUTTON_B):
        angle_servo1 = inc_serv_angle(angle_servo1, da, MAX_ANGLE_HALF, servo1)
