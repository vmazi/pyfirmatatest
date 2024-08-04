import datetime
import os

import pyfirmata
import pygame

from command_executor import execute_command
from control import generate_commands, check_record, check_end_record, check_replay, check_save_record, \
    check_print_angle, ControlInput

# set up arduino board
board = pyfirmata.Arduino('COM3')

degree_increment = .60  # initial speed (degrees per keypress)


class Servo:
    def __init__(self, angle_servo, pin):
        self.angle_servo = angle_servo
        self.servo = board.get_pin('d:' + str(pin) + ':s')


servo_init_angle = [50, 33, 47, 130, 90, 104, 50, 33, 47, 80, 90, 87]

servomotors = []


def setup_arm_control():
    for i in range(2, 14):
        servo_motor = Servo(servo_init_angle[i - 2], i)
        servo_motor.servo.write(servo_motor.angle_servo)
        servomotors.append(servo_motor)


def execute_multiple_inputs():
    command_buffer = generate_commands()
    for command in command_buffer:
        execute_command(command, servomotors, degree_increment)


def main():
    setup_arm_control()
    events = []

    clock = pygame.time.Clock()
    while True:
        clock.tick(120)

        check_print_angle(servomotors)

        execute_multiple_inputs()


if __name__ == "__main__":
    main()
