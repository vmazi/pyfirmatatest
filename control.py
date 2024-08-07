import time
from enum import Enum

import keyboard
import pygame

DEADZONE = .2

MIN_ANGLE = 10

MAX_ANGLE_FULL = 180

MAX_ANGLE_HALF = 110


class ControlInput(Enum):
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

    DIRECT_SELECT_TOOL = "DIRECT_SELECT_TOOL"

    DIRECT_MOVE_TO_INIT = "DIRECT_MOVE_TO_INIT"

    MACRO_GRAB_INGREDIENT = "MACRO_GRAB_INGREDIENT"

    MACRO_TOOL_SELECT = "MACRO_TOOL_SELECT"


def check_print_angle(servomotors):
    if keyboard.is_pressed('p'):
        for index in range(0, len(servomotors)):
            print('servo:' + str(index) + ' has angle: ', str(servomotors[index].angle_servo))


def check_end_record(currently_recording):
    if currently_recording:
        if keyboard.is_pressed('t'):
            print("done record")
            return False
        else:
            return True


def check_replay():
    if keyboard.is_pressed('e'):
        print("replaying!")
        return True


def check_record():
    if keyboard.is_pressed('r'):
        print("recording!")
        return True


def check_save_record():
    if keyboard.is_pressed('s'):
        print("will save on replay")
        return True


# def check_tool_ing_execute(buffer):
#     if get_button(9):
#         buffer.append(ControlInput.MACRO_GRAB_INGREDIENT)


def check_black_claw_grab(buffer):
    if keyboard.is_pressed('n'):
        buffer.append(ControlInput.BLACK_CLAW_GRAB_INC)
    elif keyboard.is_pressed('m'):
        buffer.append(ControlInput.BLACK_CLAW_GRAB_DEC)


def check_black_claw_rotate(buffer):
    if keyboard.is_pressed('h'):
        buffer.append(ControlInput.BLACK_CLAW_ROT_INC)
    elif keyboard.is_pressed('j'):
        buffer.append(ControlInput.BLACK_CLAW_ROT_DEC)


def check_black_tert_vert(buffer):
    if keyboard.is_pressed('y'):
        buffer.append(ControlInput.BLACK_TERT_VERT_DEC)
    elif keyboard.is_pressed('u'):
        buffer.append(ControlInput.BLACK_TERT_VERT_INC)


def check_black_secondary_vert(buffer):
    if keyboard.is_pressed(','):
        buffer.append(ControlInput.BLACK_SEC_VERT_INC)
    elif keyboard.is_pressed('.'):
        buffer.append(ControlInput.BLACK_SEC_VERT_DEC)


def check_black_primary_vert(buffer):
    if keyboard.is_pressed('k'):
        buffer.append(ControlInput.BLACK_PRI_VERT_INC)
    elif keyboard.is_pressed('l'):
        buffer.append(ControlInput.BLACK_PRI_VERT_DEC)


def check_black_base_rotate(buffer):
    if keyboard.is_pressed('i'):
        buffer.append(ControlInput.BLACK_BASE_ROT_INC)
    elif keyboard.is_pressed('o'):
        buffer.append(ControlInput.BLACK_BASE_ROT_DEC)


def check_claw_grab(buffer):
    if keyboard.is_pressed('v'):
        buffer.append(ControlInput.SILVER_CLAW_GRAB_INC)
    elif keyboard.is_pressed('b'):
        buffer.append(ControlInput.SILVER_CLAW_GRAB_DEC)


def check_claw_rotate(buffer):
    if keyboard.is_pressed('f'):
        buffer.append(ControlInput.SILVER_CLAW_ROT_INC)
    elif keyboard.is_pressed('g'):
        buffer.append(ControlInput.SILVER_CLAW_ROT_DEC)


def check_tert_vert(buffer):
    if keyboard.is_pressed('r'):
        buffer.append(ControlInput.SILVER_TERT_VERT_DEC)
    elif keyboard.is_pressed('t'):
        buffer.append(ControlInput.SILVER_TERT_VERT_INC)


def check_secondary_vert(buffer):
    if keyboard.is_pressed('x'):
        buffer.append(ControlInput.SILVER_SEC_VERT_INC)
    elif keyboard.is_pressed('c'):
        buffer.append(ControlInput.SILVER_SEC_VERT_DEC)


def check_primary_vert(buffer):
    if keyboard.is_pressed('s'):
        buffer.append(ControlInput.SILVER_PRI_VERT_INC)
    elif keyboard.is_pressed('d'):
        buffer.append(ControlInput.SILVER_PRI_VERT_DEC)


def check_base_rotate(buffer):
    if keyboard.is_pressed('w'):
        buffer.append(ControlInput.SILVER_BASE_ROT_INC)
    elif keyboard.is_pressed('e'):
        buffer.append(ControlInput.SILVER_BASE_ROT_DEC)


# def check_move_to_tool_select(command_buffer):
#     if et_button(8):
#         command_buffer.append(ControlInput.DIRECT_SELECT_TOOL)


# def check_move_to_init(command_buffer):
#     if et_button(7):
#         command_buffer.append(ControlInput.DIRECT_MOVE_TO_INIT)


def check_stick_up(x_axis, y_axis):
    return y_axis < -DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_down(x_axis, y_axis):
    return y_axis > DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_left(x_axis, y_axis):
    return x_axis < -DEADZONE and abs(x_axis) > abs(y_axis)


def check_stick_right(x_axis, y_axis):
    return x_axis > DEADZONE and abs(x_axis) > abs(y_axis)


def generate_commands():
    command_buffer = []

    check_claw_grab(command_buffer)

    check_claw_rotate(command_buffer)

    check_tert_vert(command_buffer)

    check_secondary_vert(command_buffer)

    check_primary_vert(command_buffer)

    check_base_rotate(command_buffer)

    check_black_claw_grab(command_buffer)

    check_black_claw_rotate(command_buffer)

    check_black_tert_vert(command_buffer)

    check_black_secondary_vert(command_buffer)

    check_black_primary_vert(command_buffer)

    check_black_base_rotate(command_buffer)

    # check_move_to_tool_select( command_buffer)
    #
    # check_move_to_init( command_buffer)

    # check_tool_ing_execute( command_buffer)

    return command_buffer
