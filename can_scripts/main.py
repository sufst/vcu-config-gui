import can
import threading
from time import sleep
from sim import *
from constants import *
from can_handlers import *

# Flag to signal threads to stop
stop_event = threading.Event()

# Flag to signal threads to start r2d
r2d_event = threading.Event()

# Flag to signal threads to start ts_on
ts_on_event = threading.Event()

# Flag to signal threads to start endurance
start_event = threading.Event()

# Mutex for vcu_simulated_messages
vcu_mutex = threading.Lock()

vcu_simulated_messages = {
  "sim_torque_request":0,
  "sim_apps":0,
  "sim_bps":0,
  "sim_r2d":0,
  "sim_ts_on":0
}


vcu_simulated_messages_test = {
  "sim_torque_request":0,
  "sim_apps":0,
  "sim_bps":0,
  "sim_r2d":0,
  "sim_ts_on":0
}

def terminate_thread():
  try:
    start_event.set()
    stop_event.set()
    ts_on_event.set()
    r2d_event.set()
  except Exception as e:
    print(f"Couldn't terminate threads: {e}")
  return

def main_thread():
  '''Main thread: Initialises can thread and updates simulated VCU messages.'''
  try:
    can_t = threading.Thread(target = canThread)
    can_t.start() # Start the CAN thread
    try:
      print("Press 't' to turn TS ON.\n")
      ts_on_event.wait()
      # Set the simulated messages to TS ON
      with vcu_mutex:
        vcu_simulated_messages.clear()
        vcu_simulated_messages.update(ts_on())
      # Wait to simulate pressing the button for 1 second
      sleep(1)
      # Reset to NULL
      with vcu_mutex:
        vcu_simulated_messages.clear()
        vcu_simulated_messages.update(NULL_VCU_SIMULATED_DATA)

      print("Press 'r' to turn R2D ON.\n")
      r2d_event.wait()
      # Set the simulated messages to R2D ON
      with vcu_mutex:
        vcu_simulated_messages.clear()
        vcu_simulated_messages.update(r2d())
      # Wait to simulate pressing the button for 1 second
      sleep(1)
      # Reset to NULL
      with vcu_mutex:
        vcu_simulated_messages.clear()
        vcu_simulated_messages.update(NULL_VCU_SIMULATED_DATA)

      print("Press 's' to start endurance simulation.\n")
      while not start_event.is_set():
        sleep(1)
      start_event.wait()
      print("Starting simulations\n")
      i = 0
      while not stop_event.is_set():
        if(i>=len(endurance_data)):
          print("Endurance done...")
          terminate_thread()
          can_t.join()
          break
        try:
          currentTorque = endurance_data[i]["INV VCU Torque Command"]
        except Exception as e:
          print(f"Couldn't get torque: {e}, setting to 0")
          currentTorque = 0
        currentTorque = configureTorqueRequest(currentTorque)

        with vcu_mutex:
          vcu_simulated_messages["sim_torque_request"] = currentTorque

        sleep(EXECUTE_FREQUENCY)
        i+=1

    except Exception as e:
      print(f"Couldn't initialise a bus: {e}")
      terminate_thread()
    print("Closing application\n")
  except KeyboardInterrupt:
      print("Main thread: Stopped.")
      terminate_thread()
  can_t.join()
  print("Main thread: Stopped.")

def canThread():
  '''CAN thread: Initialises the bus and sends messages.'''
  try:
    with can.interface.Bus(interface='socketcan', channel=SERIAL_PORT_UNIX) as bus:
    # with can.interface.Bus(interface='slcan', channel='COM5', bitrate=SERIAL_BAUD_RATE) as bus:
    # with initBus() as bus:
      while not stop_event.is_set():
        with vcu_mutex:
          if sendSimulatedVCUMessage(bus, vcu_simulated_messages) is None:
            break;
        sleep(0.1)
      safeExit(bus)
  except Exception as e:
      print(e)
      print("CAN thread: Stopped.")
      terminate_thread()
      return
  finally:
    terminate_thread()
    print("CAN thread: Stopped.")


def listener_thread():
  """Listener thread: Listens for key press."""
  while not ts_on_event.is_set():
    key = input()
    if key.lower() == 't':
      print("'t' pressed, turning TS ON.\n")
      ts_on_event.set()
  while not r2d_event.is_set():
    key = input()
    if key.lower() == 'r':
      print("'r' pressed, turning R2D ON.\n")
      r2d_event.set()
  while not start_event.is_set():
    key = input()
    if key.lower() == 's':
      print("'s' pressed, starting endurance.\n")
      start_event.set()
  print("Press 'q' to stop endurance simulation.\n")
  while not stop_event.is_set():
    key = input()
    if key.lower() == 'q':
      print("'q' pressed, stopping all threads.\n")
      stop_event.set()


######## EXECUTABLE PART ################

main_t = threading.Thread(target=main_thread, daemon=True)
listener_t = threading.Thread(target=listener_thread)

main_t.start()
listener_t.start()

# Wait for threads to complete
listener_t.join()  # listener, waits for stop signal
stop_event.set()  # Ensure stop signal is sent to all threads
main_t.join()