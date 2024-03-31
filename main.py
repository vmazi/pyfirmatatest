from enum import Enum
from time import sleep

import keyboard
import pyfirmata
import pygame


class ReadInput(Enum):
    SILVER_CLAW_ROT_INC = "SILVER_CLAW_ROT_INC"
    SILVER_CLAW_ROT_DEC = "SILVER_CLAW_ROT_DEC"

    SILVER_CLAW_GRAB_INC = "SILVER_CLAW_GRAB_INC"
    SILVER_CLAW_GRAB_DEC = "SILVER_CLAW_GRAB_DEC"

    SILVER_TERT_VERT_DEC = "SILVER_TERT_VERT_DEC"
    SILVER_TERT_VERT_INC = "SILVER_TERT_VERT_INC"

    SILVER_SEC_VERT_DEC = "SILVER_SEC_VERT_DEC"
    SILVER_SEC_VERT_INC = "SILVER_SEC_VERT_INC"

    SILVER_PRI_VERT_INC = "SILVER_PRI_VERT_INC"
    SILVER_PRI_VERT_DEC = "SILVER_PRI_VERT_DEC"

    SILVER_BASE_ROT_INC = "SILVER_BASE_ROT_INC"
    SILVER_BASE_ROT_DEC = "SILVER_BASE_ROT_DEC"

    BLACK_CLAW_ROT_DEC = "BLACK_CLAW_ROT_DEC"
    BLACK_CLAW_ROT_INC = "BLACK_CLAW_ROT_INC"

    BLACK_CLAW_GRAB_INC = "BLACK_CLAW_GRAB_INC"
    BLACK_CLAW_GRAB_DEC = "BLACK_CLAW_GRAB_DEC"

    BLACK_TERT_VERT_INC = "BLACK_TERT_VERT_INC"
    BLACK_TERT_VERT_DEC = "BLACK_TERT_VERT_DEC"

    BLACK_SEC_VERT_INC = "BLACK_SEC_VERT_INC"
    BLACK_SEC_VERT_DEC = "BLACK_SEC_VERT_DEC"

    BLACK_PRI_VERT_INC = "BLACK_PRI_VERT_INC"
    BLACK_PRI_VERT_DEC = "BLACK_PRI_VERT_DEC"

    BLACK_BASE_ROT_INC = "BLACK_BASE_ROT_INC"
    BLACK_BASE_ROT_DEC = "BLACK_BASE_ROT_DEC"

    MACRO_SELECT_TOOL = "MACRO_SELECT_TOOL"


DEADZONE = .2

MIN_ANGLE = 10

MAX_ANGLE_FULL = 180

MAX_ANGLE_HALF = 110

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
    servomotors[servo_num].angle_servo = dec_serv_angle(servomotors[servo_num].angle_servo, degree_increment, min_angle,
                                                        servomotors[servo_num].servo)


def increase_servo_angle(servo_num, max_angle):
    servomotors[servo_num].angle_servo = inc_serv_angle(servomotors[servo_num].angle_servo, degree_increment, max_angle,
                                                        servomotors[servo_num].servo)


def check_silver_claw_grab(buffer):
    if keyboard.is_pressed('h'):
        buffer.append(ReadInput.SILVER_CLAW_GRAB_INC)
    elif keyboard.is_pressed('j'):
        buffer.append(ReadInput.SILVER_CLAW_GRAB_DEC)


def check_silver_claw_rotate(buffer):
    if keyboard.is_pressed('n'):
        buffer.append(ReadInput.SILVER_CLAW_ROT_INC)
    elif keyboard.is_pressed('m'):
        buffer.append(ReadInput.SILVER_CLAW_ROT_DEC)


def check_silver_tert_vert(gpad, buffer):
    if gpad.get_button(4):
        buffer.append(ReadInput.SILVER_TERT_VERT_DEC)
    elif gpad.get_button(5):
        buffer.append(ReadInput.SILVER_TERT_VERT_INC)


def check_silver_secondary_vert(gpad, buffer):
    if gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) > .5:
        buffer.append(ReadInput.SILVER_SEC_VERT_DEC)
    elif gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) > .5:
        buffer.append(ReadInput.SILVER_SEC_VERT_INC)


def check_silver_primary_vert(gpad, buffer):
    if gpad.get_hat(0) == (0, -1):
        buffer.append(ReadInput.SILVER_PRI_VERT_INC)
    elif gpad.get_hat(0) == (0, 1):
        buffer.append(ReadInput.SILVER_PRI_VERT_DEC)


def check_silver_base_rotate(gpad, buffer):
    if gpad.get_hat(0) == (-1, 0):
        buffer.append(ReadInput.SILVER_BASE_ROT_INC)
    elif gpad.get_hat(0) == (1, 0):
        buffer.append(ReadInput.SILVER_BASE_ROT_DEC)


def check_claw_grab(gpad, buffer):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_A):
        buffer.append(ReadInput.BLACK_CLAW_GRAB_INC)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_B):
        buffer.append(ReadInput.BLACK_CLAW_GRAB_DEC)


def check_claw_rotate(gpad, buffer):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_X):
        buffer.append(ReadInput.BLACK_CLAW_ROT_DEC)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_Y):
        buffer.append(ReadInput.BLACK_CLAW_ROT_INC)


def check_tert_vert(gamepad, buffer):
    horizontal_axis_l = gamepad.get_axis(0)
    vertical_axis_l = gamepad.get_axis(1)

    if check_stick_left(horizontal_axis_l, vertical_axis_l):
        buffer.append(ReadInput.BLACK_TERT_VERT_DEC)
    elif check_stick_right(horizontal_axis_l, vertical_axis_l):
        buffer.append(ReadInput.BLACK_TERT_VERT_INC)


def check_secondary_vert(gamepad, buffer):
    horizontal_axis_l = gamepad.get_axis(0)
    vertical_axis_l = gamepad.get_axis(1)

    if check_stick_up(horizontal_axis_l, vertical_axis_l):
        buffer.append(ReadInput.BLACK_SEC_VERT_INC)
    elif check_stick_down(horizontal_axis_l, vertical_axis_l):
        buffer.append(ReadInput.BLACK_SEC_VERT_DEC)


def check_primary_vert(gamepad, buffer):
    horizontal_axis_r = gamepad.get_axis(2)
    vertical_axis_r = gamepad.get_axis(3)
    if check_stick_down(horizontal_axis_r, vertical_axis_r):
        buffer.append(ReadInput.BLACK_PRI_VERT_INC)
    elif check_stick_up(horizontal_axis_r, vertical_axis_r):
        buffer.append(ReadInput.BLACK_PRI_VERT_DEC)


def check_base_rotate(gamepad, buffer):
    horizontal_axis_r = gamepad.get_axis(2)
    vertical_axis_r = gamepad.get_axis(3)
    if check_stick_left(horizontal_axis_r, vertical_axis_r):
        buffer.append(ReadInput.BLACK_BASE_ROT_INC)
    elif check_stick_right(horizontal_axis_r, vertical_axis_r):
        buffer.append(ReadInput.BLACK_BASE_ROT_DEC)


def check_move_to_tool_select(gpad, command_buffer):
    if gpad.get_button(8):
        command_buffer.append(ReadInput.MACRO_SELECT_TOOL)


def generate_commands(gamepad):
    command_buffer = []

    check_claw_grab(gamepad, command_buffer)

    check_claw_rotate(gamepad, command_buffer)

    check_tert_vert(gamepad, command_buffer)

    check_secondary_vert(gamepad, command_buffer)

    check_primary_vert(gamepad, command_buffer)

    check_base_rotate(gamepad, command_buffer)

    check_silver_claw_grab(command_buffer)

    check_silver_claw_rotate(command_buffer)

    check_silver_tert_vert(gamepad, command_buffer)

    check_silver_secondary_vert(gamepad, command_buffer)

    check_silver_primary_vert(gamepad, command_buffer)

    check_silver_base_rotate(gamepad, command_buffer)

    check_move_to_tool_select(gamepad, command_buffer)
    return command_buffer


def execute_black_arm_command(input_command):
    match input_command:
        case ReadInput.BLACK_BASE_ROT_INC:
            increase_servo_angle(5, 167)
        case ReadInput.BLACK_BASE_ROT_DEC:
            decrease_servo_angle(5, 36.5)
        case ReadInput.BLACK_PRI_VERT_INC:
            increase_servo_angle(4, MAX_ANGLE_FULL)
        case ReadInput.BLACK_PRI_VERT_DEC:
            decrease_servo_angle(4, MIN_ANGLE)
        case ReadInput.BLACK_SEC_VERT_INC:
            increase_servo_angle(3, MAX_ANGLE_FULL)
        case ReadInput.BLACK_SEC_VERT_DEC:
            decrease_servo_angle(3, MIN_ANGLE)
        case ReadInput.BLACK_TERT_VERT_INC:
            increase_servo_angle(2, MAX_ANGLE_FULL)
        case ReadInput.BLACK_TERT_VERT_DEC:
            decrease_servo_angle(2, MIN_ANGLE)
        case ReadInput.BLACK_CLAW_ROT_INC:
            increase_servo_angle(1, MAX_ANGLE_FULL)
        case ReadInput.BLACK_CLAW_ROT_DEC:
            decrease_servo_angle(1, MIN_ANGLE)
        case ReadInput.BLACK_CLAW_GRAB_INC:
            increase_servo_angle(0, 88)
        case ReadInput.BLACK_CLAW_GRAB_DEC:
            decrease_servo_angle(0, 40)


def execute_silver_arm_command(input_command):
    match input_command:
        case ReadInput.SILVER_BASE_ROT_INC:
            increase_servo_angle(11, 167)
        case ReadInput.SILVER_BASE_ROT_DEC:
            decrease_servo_angle(11, 36.5)
        case ReadInput.SILVER_PRI_VERT_INC:
            increase_servo_angle(10, MAX_ANGLE_FULL)
        case ReadInput.SILVER_PRI_VERT_DEC:
            decrease_servo_angle(10, MIN_ANGLE)
        case ReadInput.SILVER_SEC_VERT_INC:
            increase_servo_angle(9, MAX_ANGLE_FULL)
        case ReadInput.SILVER_SEC_VERT_DEC:
            decrease_servo_angle(9, MIN_ANGLE)
        case ReadInput.SILVER_TERT_VERT_INC:
            increase_servo_angle(8, MAX_ANGLE_FULL)
        case ReadInput.SILVER_TERT_VERT_DEC:
            decrease_servo_angle(8, MIN_ANGLE)
        case ReadInput.SILVER_CLAW_ROT_INC:
            increase_servo_angle(7, MAX_ANGLE_FULL)
        case ReadInput.SILVER_CLAW_ROT_DEC:
            decrease_servo_angle(7, MIN_ANGLE)
        case ReadInput.SILVER_CLAW_GRAB_INC:
            increase_servo_angle(6, 88)
        case ReadInput.SILVER_CLAW_GRAB_DEC:
            decrease_servo_angle(6, 40)


def execute_macro_command(input_command):
    match input_command:
        case ReadInput.MACRO_SELECT_TOOL:
            tool_grab_pose = [{'ind': 6, 'angle': 40.5}, {'ind': 7, 'angle': 124.5}, {'ind': 8, 'angle': 141.5},
                              {'ind': 9, 'angle': 101.0}, {'ind': 10, 'angle': 107.5},
                              {'ind': 11, 'lag': .5, 'angle': 118.0}]
            move_arm_to_pos(tool_grab_pose)


def execute_command(input_command):
    if input_command.value.startswith("BLACK"):
        execute_black_arm_command(input_command)
    elif input_command.value.startswith("SILVER"):
        execute_silver_arm_command(input_command)
    else:
        execute_macro_command(input_command)


def check_move_to_stance():
    if keyboard.is_pressed('s'):
        hold_pose = [{'ind': 6, 'angle': 40.5}, {'ind': 7, 'angle': 124.5}, {'ind': 8, 'angle': 141.5},
                     {'ind': 9, 'angle': 101.0}, {'ind': 10, 'angle': 107.5}, {'ind': 11, 'lag': .5, 'angle': 118.0}]
        move_arm_to_pos(hold_pose)


def check_move_to_init(gpad):
    if gpad.get_button(7):
        hold_pose = [{'ind': 5, 'angle': 104}, {'ind': 0, 'angle': 50}, {'ind': 1, 'angle': 33},
                     {'ind': 2, 'angle': 47}, {'ind': 3, 'angle': 130}, {'ind': 4, 'angle': 90}]
        move_arm_to_pos(hold_pose)
        hold_pose = [{'ind': 11, 'angle': 87}, {'ind': 6, 'angle': 50}, {'ind': 7, 'angle': 33},
                     {'ind': 8, 'angle': 47}, {'ind': 9, 'angle': 80}, {'ind': 10, 'angle': 90}]
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


def check_replay(currently_replaying):
    if currently_replaying:
        return currently_replaying
    if keyboard.is_pressed('e'):
        print("replaying!")
        return True


def check_record(currently_recording):
    if currently_recording:
        return currently_recording
    if keyboard.is_pressed('r'):
        print("recording!")
        return True


def check_end_record(currently_recording):
    if currently_recording:
        if keyboard.is_pressed('t'):
            print("done record")
            return False
        else:
            return True


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
        check_move_to_stance()
        check_move_to_init(gamepad)

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
