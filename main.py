import time

import keyboard
import pyfirmata
import pygame

from command import execute_command
from control import generate_commands, check_record, check_end_record, check_replay, check_save_record
from move_servo import dec_serv_angle, inc_serv_angle, move_servo

# set up arduino board
board = pyfirmata.Arduino('COM3')

degree_increment = .5  # initial speed (degrees per keypress)


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


def decrease_servo_angle(servo_num, min_angle):
    servomotors[servo_num].angle_servo = dec_serv_angle(servomotors[servo_num].angle_servo, degree_increment, min_angle,
                                                        servomotors[servo_num].servo)


def increase_servo_angle(servo_num, max_angle):
    servomotors[servo_num].angle_servo = inc_serv_angle(servomotors[servo_num].angle_servo, degree_increment, max_angle,
                                                        servomotors[servo_num].servo)


# def check_move_to_stance():
#     if keyboard.is_pressed('s'):
#         hold_pose = [{'ind': 6, 'angle': 40.5}, {'ind': 7, 'angle': 124.5}, {'ind': 8, 'angle': 141.5},
#                      {'ind': 9, 'angle': 101.0}, {'ind': 10, 'angle': 107.5}, {'ind': 11, 'lag': .5, 'angle': 118.0}]
#         move_arm_to_pos(hold_pose)


def move_arm_to_pos(desired_pose):
    for increment in range(6):
        if 'lag' in desired_pose[increment]:
            time.sleep(desired_pose[increment].get('lag'))

        move_servo_to_angle(desired_pose[increment].get('ind'), desired_pose[increment].get('angle'))


def move_servo_to_angle(servo_ind, angle_to_set):
    servomotors[servo_ind].angle_servo = angle_to_set
    move_servo(servomotors[servo_ind].servo, servomotors[servo_ind].angle_servo)


# def check_chop_input():
#     if keyboard.is_pressed('c'):
#         servomotors[2].angle_servo = 35.0
#         move_servo(servomotors[2].servo, servomotors[2].angle_servo)
#         servomotors[4].angle_servo = 82.0
#         move_servo(servomotors[4].servo, servomotors[4].angle_servo)
#

def check_print_angle(gpad):
    if keyboard.is_pressed('p'):
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT))
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT))
        for index in range(0, len(servomotors)):
            print('servo:' + str(index) + ' has angle: ', str(servomotors[index].angle_servo))


def main():
    joysticks = setup_arm_control()
    events = []
    # %% while loop
    gamepad = joysticks[-1]

    clock = pygame.time.Clock()
    record_to_buffer = False
    replay_buffer = False
    recorded_buffer = []
    while True:
        clock.tick(120)

        new_events = pygame.event.get()
        if len(new_events) != 0:
            events = new_events  # for event in events:  #     print(event)

        if gamepad.get_button(9):
            print('right stick pressed')

        record_to_buffer = check_record(record_to_buffer)
        record_to_buffer = check_end_record(record_to_buffer)

        replay_buffer = check_replay(replay_buffer)

        check_print_angle(gamepad)
        check_save_record(recorded_buffer)

        if replay_buffer:
            if len(recorded_buffer) == 0:
                replay_buffer = False
                print("finished replaying!")
            else:
                replay_commands = recorded_buffer.pop(0)
                for command in replay_commands:
                    execute_command(command)
        else:
            command_buffer = generate_commands(gamepad)
            for command in command_buffer:
                execute_command(command)
            if record_to_buffer:
                recorded_buffer.append(command_buffer)


if __name__ == "__main__":
    main()
