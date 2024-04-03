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


def check_print_angle(gpad, servomotors):
    if keyboard.is_pressed('p'):
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT))
        print(gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT))
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


def check_macro_execute(buffer):
    if keyboard.is_pressed('x'):
        buffer.append(ControlInput.MACRO_GRAB_INGREDIENT)


def check_silver_claw_grab(buffer):
    if keyboard.is_pressed('h'):
        buffer.append(ControlInput.SILVER_CLAW_GRAB_INC)
    elif keyboard.is_pressed('j'):
        buffer.append(ControlInput.SILVER_CLAW_GRAB_DEC)


def check_silver_claw_rotate(buffer):
    if keyboard.is_pressed('n'):
        buffer.append(ControlInput.SILVER_CLAW_ROT_INC)
    elif keyboard.is_pressed('m'):
        buffer.append(ControlInput.SILVER_CLAW_ROT_DEC)


def check_silver_tert_vert(gpad, buffer):
    if gpad.get_button(4):
        buffer.append(ControlInput.SILVER_TERT_VERT_DEC)
    elif gpad.get_button(5):
        buffer.append(ControlInput.SILVER_TERT_VERT_INC)


def check_silver_secondary_vert(gpad, buffer):
    if gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) > .5:
        buffer.append(ControlInput.SILVER_SEC_VERT_DEC)
    elif gpad.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) > .5:
        buffer.append(ControlInput.SILVER_SEC_VERT_INC)


def check_silver_primary_vert(gpad, buffer):
    if gpad.get_hat(0) == (0, -1):
        buffer.append(ControlInput.SILVER_PRI_VERT_INC)
    elif gpad.get_hat(0) == (0, 1):
        buffer.append(ControlInput.SILVER_PRI_VERT_DEC)


def check_silver_base_rotate(gpad, buffer):
    if gpad.get_hat(0) == (-1, 0):
        buffer.append(ControlInput.SILVER_BASE_ROT_INC)
    elif gpad.get_hat(0) == (1, 0):
        buffer.append(ControlInput.SILVER_BASE_ROT_DEC)


def check_claw_grab(gpad, buffer):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_A):
        buffer.append(ControlInput.BLACK_CLAW_GRAB_INC)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_B):
        buffer.append(ControlInput.BLACK_CLAW_GRAB_DEC)


def check_claw_rotate(gpad, buffer):
    if gpad.get_button(pygame.CONTROLLER_BUTTON_X):
        buffer.append(ControlInput.BLACK_CLAW_ROT_DEC)
    elif gpad.get_button(pygame.CONTROLLER_BUTTON_Y):
        buffer.append(ControlInput.BLACK_CLAW_ROT_INC)


def check_tert_vert(gamepad, buffer):
    horizontal_axis_l = gamepad.get_axis(0)
    vertical_axis_l = gamepad.get_axis(1)

    if check_stick_left(horizontal_axis_l, vertical_axis_l):
        buffer.append(ControlInput.BLACK_TERT_VERT_DEC)
    elif check_stick_right(horizontal_axis_l, vertical_axis_l):
        buffer.append(ControlInput.BLACK_TERT_VERT_INC)


def check_secondary_vert(gamepad, buffer):
    horizontal_axis_l = gamepad.get_axis(0)
    vertical_axis_l = gamepad.get_axis(1)

    if check_stick_up(horizontal_axis_l, vertical_axis_l):
        buffer.append(ControlInput.BLACK_SEC_VERT_INC)
    elif check_stick_down(horizontal_axis_l, vertical_axis_l):
        buffer.append(ControlInput.BLACK_SEC_VERT_DEC)


def check_primary_vert(gamepad, buffer):
    horizontal_axis_r = gamepad.get_axis(2)
    vertical_axis_r = gamepad.get_axis(3)
    if check_stick_down(horizontal_axis_r, vertical_axis_r):
        buffer.append(ControlInput.BLACK_PRI_VERT_INC)
    elif check_stick_up(horizontal_axis_r, vertical_axis_r):
        buffer.append(ControlInput.BLACK_PRI_VERT_DEC)


def check_base_rotate(gamepad, buffer):
    horizontal_axis_r = gamepad.get_axis(2)
    vertical_axis_r = gamepad.get_axis(3)
    if check_stick_left(horizontal_axis_r, vertical_axis_r):
        buffer.append(ControlInput.BLACK_BASE_ROT_INC)
    elif check_stick_right(horizontal_axis_r, vertical_axis_r):
        buffer.append(ControlInput.BLACK_BASE_ROT_DEC)


def check_move_to_tool_select(gpad, command_buffer):
    if gpad.get_button(8):
        command_buffer.append(ControlInput.DIRECT_SELECT_TOOL)


def check_move_to_init(gpad, command_buffer):
    if gpad.get_button(7):
        command_buffer.append(ControlInput.DIRECT_MOVE_TO_INIT)


def check_stick_up(x_axis, y_axis):
    return y_axis < -DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_down(x_axis, y_axis):
    return y_axis > DEADZONE and abs(y_axis) > abs(x_axis)


def check_stick_left(x_axis, y_axis):
    return x_axis < -DEADZONE and abs(x_axis) > abs(y_axis)


def check_stick_right(x_axis, y_axis):
    return x_axis > DEADZONE and abs(x_axis) > abs(y_axis)


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

    check_move_to_init(gamepad, command_buffer)

    check_macro_execute(command_buffer)

    return command_buffer
