from enum import Enum

import keyboard
import pygame

from control import MAX_ANGLE_FULL, MIN_ANGLE, check_stick_down, check_stick_up, check_stick_right, check_stick_left, \
    ReadInput
from main import increase_servo_angle, decrease_servo_angle, move_arm_to_pos



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


def execute_direct_command(input_command):
    match input_command:
        case ReadInput.DIRECT_SELECT_TOOL:
            tool_grab_pose = [{'ind': 6, 'angle': 40.5}, {'ind': 7, 'angle': 124.5}, {'ind': 8, 'angle': 141.5},
                              {'ind': 9, 'angle': 101.0}, {'ind': 10, 'angle': 107.5},
                              {'ind': 11, 'lag': .5, 'angle': 118.0}]
            move_arm_to_pos(tool_grab_pose)
        case ReadInput.DIRECT_MOVE_TO_INIT:
            hold_pose = [{'ind': 5, 'angle': 104}, {'ind': 0, 'angle': 50}, {'ind': 1, 'angle': 33},
                         {'ind': 2, 'angle': 47}, {'ind': 3, 'angle': 130}, {'ind': 4, 'angle': 90}]
            move_arm_to_pos(hold_pose)
            hold_pose = [{'ind': 11, 'angle': 87}, {'ind': 6, 'angle': 50}, {'ind': 7, 'angle': 33},
                         {'ind': 8, 'angle': 47}, {'ind': 9, 'angle': 80}, {'ind': 10, 'angle': 90}]
            move_arm_to_pos(hold_pose)


def execute_command(input_command):
    if input_command.value.startswith("BLACK"):
        execute_black_arm_command(input_command)
    elif input_command.value.startswith("SILVER"):
        execute_silver_arm_command(input_command)
    else:
        execute_direct_command(input_command)
