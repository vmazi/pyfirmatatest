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


def is_file_macro(file_name):
    try:
        ControlInput(file_name.split(".")[0])
        return True
    except ValueError:
        return False


def load_macros():
    macro_map = {}
    macro_path = "macros"
    file_list = os.listdir(macro_path)
    for file_name in file_list:
        if is_file_macro(file_name):
            macro_name = ControlInput(file_name.split(".")[0]).value
            macro_commands = []
            with open(macro_path + os.sep + file_name, "r") as macro_file:
                for line in macro_file.readlines():
                    if line.isspace():
                        macro_commands.append([])
                    else:
                        line_commands = line.replace("\n", "").split(" ")
                        cleaned_commands = []
                        possible_commands = [c.value for c in ControlInput]
                        for command in line_commands:
                            if command in possible_commands:
                                cleaned_commands.append(command)
                        macro_commands.append(cleaned_commands)
                macro_map[macro_name] = macro_commands
    print("loaded macros: " + str(macro_map.keys()))
    return macro_map


def run_macro_tick(macro_command_buffer, macro_map):
    macro_commands = macro_command_buffer[-1]
    macro_position = len(macro_command_buffer) - 1
    command_set = macro_commands.pop(0)
    for command in command_set:
        new_macro_commands = execute_command(ControlInput(command), servomotors, degree_increment, macro_map)
        if len(new_macro_commands) > 0:
            macro_command_buffer.append(new_macro_commands)
    if len(macro_commands) == 0:
        macro_command_buffer.pop(macro_position)


def execute_gamepad_inputs(gamepad, record_to_buffer, recorded_buffer, macro_map):
    command_buffer = generate_commands(gamepad)
    found_macro_commands = []
    for command in command_buffer:
        new_macro_commands = execute_command(command, servomotors, degree_increment, macro_map)
        if len(new_macro_commands) > 0:
            found_macro_commands.append(new_macro_commands)
    if record_to_buffer:
        recorded_buffer.append(command_buffer)
    return found_macro_commands


def replay_command_from_buffer(recorded_buffer, save_buffer, save_on_replay, macro_map):
    replay_commands = recorded_buffer.pop(0)
    found_macro_commands = []
    if save_on_replay:
        save_buffer.append(replay_commands)
    for command in replay_commands:
        new_macro_commands = execute_command(command, servomotors, degree_increment, macro_map)
        if len(new_macro_commands) > 0:
            found_macro_commands.append(new_macro_commands)
    return found_macro_commands


def save_replay_to_file(save_buffer):
    saved_file_name = (str(datetime.datetime.now()).replace(" ", "T").replace(":", "_") + "_saved_macro.txt")
    with open(saved_file_name, "w") as file:
        for save_commands in save_buffer:
            for command in save_commands:
                file.write(command.value + " ")
            file.write("\n")
        print("saved this replay as: " + saved_file_name)


def main():
    joysticks = setup_arm_control()
    events = []
    # %% while loop
    gamepad = joysticks[-1]

    clock = pygame.time.Clock()
    record_to_buffer_requested = False
    replay_buffer_requested = False
    recorded_buffer = []
    save_on_replay_requested = False
    save_buffer = []
    macro_map = load_macros()

    macro_command_buffer = []
    while True:
        clock.tick(120)

        new_events = pygame.event.get()
        if len(new_events) != 0:
            events = new_events  # for event in events:  #     print(event)

        if len(macro_command_buffer) > 0:
            run_macro_tick(macro_command_buffer, macro_map)
            continue

        if not record_to_buffer_requested:
            record_to_buffer_requested = check_record()

        record_to_buffer_requested = check_end_record(record_to_buffer_requested)

        if not replay_buffer_requested:
            replay_buffer_requested = check_replay()

        check_print_angle(gamepad, servomotors)

        if not save_on_replay_requested:
            save_on_replay_requested = check_save_record()

        new_macro_command_buffer = []

        if replay_buffer_requested:
            if len(recorded_buffer) == 0:
                replay_buffer_requested = False
                print("finished replaying!")
                if save_on_replay_requested:
                    save_replay_to_file(save_buffer)
                    save_on_replay_requested = False
            else:
                new_macro_command_buffer = replay_command_from_buffer(recorded_buffer, save_buffer,
                                                                      save_on_replay_requested, macro_map)
        else:
            new_macro_command_buffer = execute_gamepad_inputs(gamepad, record_to_buffer_requested, recorded_buffer,
                                                              macro_map)
        if len(new_macro_command_buffer) > 0:
            macro_command_buffer.extend(new_macro_command_buffer)


if __name__ == "__main__":
    main()
