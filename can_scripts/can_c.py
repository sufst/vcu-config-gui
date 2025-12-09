from can_helpers import *

def can_c_pm100_command_message_pm100_torque_command_encode(value):
  return int(value / 0.1)

def can_c_pm100_command_message_pm100_torque_command_decode(value):
  return int(value * 0.1)

def can_c_pm100_command_message_pack(data):
  try:
    pm100_torque_command = data["pm100_torque_command"]
    pm100_speed_command = data["pm100_speed_command"]
    pm100_torque_limit_command = data["pm100_torque_limit_command"]
    pm100_direction_command = data["pm100_direction_command"]
    pm100_inverter_enable = data["pm100_inverter_enable"]
    pm100_inverter_discharge = data["pm100_inverter_discharge"]
    pm100_speed_mode_enable = data["pm100_speed_mode_enable"]
    pm100_rolling_counter = data["pm100_rolling_counter"]
  except Exception as e:
    print(e)
    return None

  packed_data = [0]*8

  packed_data[0] |= pack_left_shift_u16(pm100_torque_command, 0, 0xFF)
  packed_data[1] |= pack_right_shift_u16(pm100_torque_command, 8, 0xFF)
  packed_data[2] |= pack_left_shift_u16(pm100_speed_command, 0, 0xFF)
  packed_data[3] |= pack_right_shift_u16(pm100_speed_command, 8, 0xFF)
  packed_data[4] |= pack_left_shift_u8(pm100_direction_command, 0, 0x01)
  packed_data[5] |= pack_left_shift_u8(pm100_inverter_enable, 0, 0x01)
  packed_data[5] |= pack_left_shift_u8(pm100_inverter_discharge, 1, 0x02)
  packed_data[5] |= pack_left_shift_u8(pm100_speed_mode_enable, 2, 0x04)
  packed_data[5] |= pack_left_shift_u8(pm100_rolling_counter, 4, 0xf0)
  packed_data[6] |= pack_left_shift_u16(pm100_torque_limit_command, 0, 0xFF)
  packed_data[7] |= pack_right_shift_u16(pm100_torque_limit_command, 8, 0xFF)

  return packed_data