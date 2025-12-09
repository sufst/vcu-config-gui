from time import sleep
from constants import *
from can_c import can_c_pm100_command_message_pm100_torque_command_encode
from can_s import *
from can_handlers import sendSimulatedVCUMessage

def configureTorqueRequest(raw_torque):
  raw_torque = float(raw_torque)
  torque = can_c_pm100_command_message_pm100_torque_command_encode(raw_torque)
  apps = torque / VCU_TORQUE_SCALE_FACTOR
  torque = apps*TORQUE_SCALE_FACTOR
  torque = min(torque,TORQUE_LIMIT) # Minimise torque
  torque = max(torque, 0) # Maximise torque

  print(raw_torque,torque)

  return int(torque)

def r2d():
  return R2D_SIMULATED_DATA

def ts_on():
  return TS_ON_SIMULATED_DATA

def sendZeroTorque(bus):
  print("Sending 0 torque request\n")
  sendSimulatedVCUMessage(bus, NULL_VCU_SIMULATED_DATA)

def pressR2D(bus):
  print("Sending R2D\n")
  sendSimulatedVCUMessage(bus, R2D_SIMULATED_DATA)

def pressTSOn(bus):
  print("Sending TS ON\n")
  sendSimulatedVCUMessage(bus, TS_ON_SIMULATED_DATA)

def safeExit(bus):
  sendZeroTorque(bus) # Ensure torque is 0
  sleep(0.5)
  pressR2D(bus)
  sleep(0.5)
  pressTSOn(bus)
  sleep(0.5)
  sendZeroTorque(bus) # Ensure torque is 0
  bus.shutdown()
  return