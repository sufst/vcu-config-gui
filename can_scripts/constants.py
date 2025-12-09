EXTRACT_FREQUENCY = 0.5 # 0.5ms entry
EXECUTE_FREQUENCY = 0.5 #

METADATA_TOP_ROWS = 13

SERIAL_PORT_WINDOW = 'COM5'
SERIAL_PORT_UNIX = 'slcan0'
SERIAL_BAUD_RATE = 500000
TORQUE_SCALE_FACTOR = 15
VCU_TORQUE_SCALE_FACTOR = 15
TORQUE_LIMIT = 1500 # safety precaution

TRIMMED_ENDURANCE_TIME_START = 99

CAN_S_VCU_SIMULATION_CONFIGS = {
  "arb_id" : 0x106,
  "is_extended" : False
}

CAN_C_INV_CONFIGS = {
  "arb_id" : 0xC0,
  "is_extended" : False
}

NULL_VCU_SIMULATED_DATA = {
  "sim_torque_request":0,
  "sim_apps":0,
  "sim_bps":0,
  "sim_r2d":0,
  "sim_ts_on":0
}

TS_ON_SIMULATED_DATA = {
  "sim_torque_request":0,
  "sim_apps":0,
  "sim_bps":0,
  "sim_r2d":0,
  "sim_ts_on":1
}

R2D_SIMULATED_DATA = {
  "sim_torque_request":0,
  "sim_apps":0,
  "sim_bps":100,
  "sim_r2d":1,
  "sim_ts_on":0
}

NULL_PM100_DATA = {
  "pm100_torque_command":0,
  "pm100_speed_command":0,
  "pm100_direction_command":0,
  "pm100_inverter_enable":0,
  "pm100_speed_mode_enable":0,
  "pm100_rolling_counter":0,
  "pm100_torque_limit_command":0,
  "pm100_inverter_discharge":0,
}