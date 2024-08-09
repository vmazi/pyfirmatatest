from control import MAX_ANGLE_FULL, MIN_ANGLE, ControlInput

from move_servo import move_arm_to_pos, decrease_servo_angle, increase_servo_angle
import copy


def execute_black_arm_command(input_command, servomotors, degree_increment):
    match input_command:
        case ControlInput.BLACK_BASE_ROT_INC:
            increase_servo_angle(5, 167, servomotors, degree_increment)
        case ControlInput.BLACK_BASE_ROT_DEC:
            decrease_servo_angle(5, 36.5, servomotors, degree_increment)
        case ControlInput.BLACK_PRI_VERT_INC:
            increase_servo_angle(4, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.BLACK_PRI_VERT_DEC:
            decrease_servo_angle(4, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.BLACK_SEC_VERT_INC:
            increase_servo_angle(3, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.BLACK_SEC_VERT_DEC:
            decrease_servo_angle(3, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.BLACK_TERT_VERT_INC:
            increase_servo_angle(2, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.BLACK_TERT_VERT_DEC:
            decrease_servo_angle(2, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.BLACK_CLAW_ROT_INC:
            increase_servo_angle(1, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.BLACK_CLAW_ROT_DEC:
            decrease_servo_angle(1, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.BLACK_CLAW_GRAB_INC:
            increase_servo_angle(0, 88, servomotors, degree_increment)
        case ControlInput.BLACK_CLAW_GRAB_DEC:
            decrease_servo_angle(0, 40, servomotors, degree_increment)


def execute_silver_arm_command(input_command, servomotors, degree_increment):
    match input_command:
        case ControlInput.SILVER_BASE_ROT_INC:
            increase_servo_angle(11, 167, servomotors, degree_increment)
        case ControlInput.SILVER_BASE_ROT_DEC:
            decrease_servo_angle(11, 36.5, servomotors, degree_increment)
        case ControlInput.SILVER_PRI_VERT_INC:
            increase_servo_angle(10, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.SILVER_PRI_VERT_DEC:
            decrease_servo_angle(10, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.SILVER_SEC_VERT_INC:
            increase_servo_angle(9, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.SILVER_SEC_VERT_DEC:
            decrease_servo_angle(9, 0, servomotors, degree_increment)
        case ControlInput.SILVER_TERT_VERT_INC:
            increase_servo_angle(8, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.SILVER_TERT_VERT_DEC:
            decrease_servo_angle(8, 22, servomotors, degree_increment)
        case ControlInput.SILVER_CLAW_ROT_INC:
            increase_servo_angle(7, MAX_ANGLE_FULL, servomotors, degree_increment)
        case ControlInput.SILVER_CLAW_ROT_DEC:
            decrease_servo_angle(7, MIN_ANGLE, servomotors, degree_increment)
        case ControlInput.SILVER_CLAW_GRAB_INC:
            increase_servo_angle(6, 90, servomotors, degree_increment)
        case ControlInput.SILVER_CLAW_GRAB_DEC:
            decrease_servo_angle(6, 45, servomotors, degree_increment)


def execute_direct_command(input_command, servomotors):
    match input_command:
        case ControlInput.DIRECT_SELECT_TOOL:
            tool_grab_pose = [{'ind': 6, 'angle': 40.5}, {'ind': 7, 'angle': 109}, {'ind': 8, 'angle': 141.5},
                              {'ind': 9, 'angle': 101.0}, {'ind': 10, 'angle': 107.5},
                              {'ind': 11, 'lag': .5, 'angle': 134.0}]
            move_arm_to_pos(tool_grab_pose, servomotors)
        case ControlInput.DIRECT_MOVE_TO_INIT:
            hold_pose = [{'ind': 5, 'angle': 104}, {'ind': 0, 'angle': 50}, {'ind': 1, 'angle': 33},
                         {'ind': 2, 'angle': 47}, {'ind': 3, 'angle': 130}, {'ind': 4, 'angle': 90}]
            move_arm_to_pos(hold_pose, servomotors)
            hold_pose = [{'ind': 11, 'angle': 87}, {'ind': 6, 'angle': 50}, {'ind': 7, 'angle': 33},
                         {'ind': 8, 'angle': 47}, {'ind': 9, 'angle': 80}, {'ind': 10, 'angle': 90}]
            move_arm_to_pos(hold_pose, servomotors)


def execute_command(input_command, servomotors, degree_increment):
    if input_command.value.startswith("BLACK"):
        execute_black_arm_command(input_command, servomotors, degree_increment)
        return
    elif input_command.value.startswith("SILVER"):
        execute_silver_arm_command(input_command, servomotors, degree_increment)
        return
    elif input_command.value.startswith("DIRECT"):
        # execute_direct_command(input_command, servomotors)
        return # else:  #      return execute_macro_command(input_command, macro_map)
