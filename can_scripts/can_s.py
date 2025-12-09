from can_helpers import *

def can_s_vcu_simulated_pack(data):
  try:
    sim_torque_request = data["sim_torque_request"]
    sim_apps = data["sim_apps"]
    sim_bps = data["sim_bps"]
    sim_r2d = data["sim_r2d"]
    sim_ts_on = data["sim_ts_on"]
  except Exception as e:
    print(f"Error: {e}")
    return None

  packed_data = [0]*8

  packed_data[0] |= pack_left_shift_u16(sim_torque_request, 0, 0xFF)
  packed_data[1] |= pack_right_shift_u16(sim_torque_request, 8, 0xFF)
  packed_data[2] |= pack_left_shift_u16(sim_apps, 0, 0xff)
  packed_data[3] |= pack_right_shift_u16(sim_apps, 8, 0xff)
  packed_data[4] |= pack_left_shift_u16(sim_bps, 0, 0xff)
  packed_data[5] |= pack_right_shift_u16(sim_bps, 8, 0xff)
  packed_data[6] |= pack_left_shift_u8(sim_r2d, 0, 0x01)
  packed_data[7] |= pack_left_shift_u8(sim_ts_on, 1, 0x02)

  return packed_data