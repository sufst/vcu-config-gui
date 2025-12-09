import can
import sys
from constants import *
from can_c import can_c_pm100_command_message_pack, can_c_pm100_command_message_pm100_torque_command_encode
from can_s import *

class MockBus:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

def initBus():
  # return MockBus()
  print(f"Connecting to the CAN Bus on {sys.platform}\n")
  if sys.platform.startswith('linux'):
    bus = can.Bus(interface="socketcan", channel="can0")
  elif sys.platform.startswith('win32'):
    bus = can.interface.Bus(interface='slcan', channel="COM9", bitrate=SERIAL_BAUD_RATE)
  elif sys.platform.startswith('darwin'):
    print("Not implemented for MacOS")
    raise can.CanInitializationError
  else:
    print(f"Unrecognised platform: {sys.platform}")
    raise can.CanInitializationError
  return bus


def sendPM100Message(bus, data):
  packed_data = can_c_pm100_command_message_pack(data)
  if packed_data is None: return  # TODO: Replace with throwing custom error

  msg = generateMessage(CAN_C_INV_CONFIGS, packed_data)
  if msg is None: return  # TODO: Replace with throwing custom error

  print(data, packed_data,msg)
  return sendMessage(bus, msg)

#does send an actualy can message
def sendVCUMessage(bus, data):
  packed_data = can_s_vcu_simulated_pack(data)
  if packed_data is None: return  # TODO: Replace with throwing custom error

  msg = generateMessage(CAN_S_VCU_SIMULATION_CONFIGS, packed_data)
  if msg is None: return  # TODO: Replace with throwing custom error

  print(data, packed_data,msg)
  return sendMessage(bus, msg)

def generateMessage(config, packed_data):
  msg = can.Message(
    arbitration_id=config["arb_id"],
    data=packed_data,
    is_extended_id=config["is_extended"]
  )
  return msg

def sendMessage(bus, msg):
  try:
    bus.send(msg)
    print(f"Message sent on {bus.channel_info}")
    return msg
  except can.CanError:
    print("Message was not sent")
    return None