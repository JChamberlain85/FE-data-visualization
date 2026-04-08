import eel
import socket
import threading
import pandas as pd
import csv
from screeninfo import get_monitors

monitor = get_monitors()
monitors = get_monitors()
for monitor in monitors:
    width = monitor.width
    height = monitor.height



#CONFIG
IP_ADDRESS = "192.168.4.1"
PORT = 80
TARGET_COUNT = 71 
CSV_FILE = 'fe_sample.csv'
eel.init('web')
eel.start(
    'index.html',
    size=(width, height),
    position=(100, 100),
    block=True
)


f = open(CSV_FILE, "w+")
f.close()


COLUMNS = [
    "Time",
    "Suspension travel FR (analog)",
    "Wheel Speed FR",
    "Rotor Temp FR",
    "Wheel temp FR",
    "Steering Angle FL (analog)",
    "Suspension travel FL (analog)",
    "Wheel Speed FL",
    "Rotor Temp FL",
    "Wheel temp FL",
    "Air Pressure FL",
    "Suspension travel BR (analog)",
    "Wheel Speed BR",
    "Rotor Temp BR",
    "Wheel temp BR",
    "Air Pressure BR",
    "Suspension travel BL (analog)",
    "Wheel Speed BL",
    "Rotor Temp BL",
    "Wheel temp BL",
    "Fluid Temp BL",
    "Fusebox Sensor 1",
    "Fusebox Sensor 2",
    "Fusebox Sensor 3",
    "Fusebox Sensor 4",
    "Fusebox Sensor 5",
    "Fusebox Sensor 6",
    "Fusebox Sensor 7",
    "Fusebox Sensor 8",
    "Fusebox Sensor 9",
    "Fusebox Sensor 10",
    "Fusebox Sensor 11",
    "Fusebox Sensor 12",
    "Fusebox Sensor 13",
    "Throttle 1 Raw",
    "Throttle 2 Raw",
    "Throttle 1",
    "Throttle 2",
    "Front Brake Raw",
    "Rear Brake Raw",
    "Motor Controller temp",
    "Motor Temp",
    "Battery Temp",
    "Low Volt Battery Temp",
    "Motor Speed",
    "Battery Voltage",
    "Current Drive Mode",
    "Ignition One state",
    "Ignition Two State",
    "Ams Fault Can",
    "IMD Fault Can",
    "BSPD Fault",
    "Brake Light",
    "Phase A Current",
    "Phase B Current",
    "Phase C Current",
    "DC Bus Current",
    "Commanded Torque",
    "Torque Feedback",
    "Soft Plausibility",
    "High Sense",
    "Current Car State",
    "QBAI",
    "Plausibility Fault",
    "Hard Brake",
    "Shut Down Circuit",
    "Battery State Of Charge",
    "Battery Current",
    "Torque",
    "Difference in Two throttles",
    "extra"
]

def background_data_collection():
    print(f"Attempting to connect to {IP_ADDRESS}...")
    
    sock = socket.socket()
    sock.settimeout(10)

    # writes columns
    with open(CSV_FILE, 'a', newline = '') as f:
        writer = csv.writer(f)

        writer.writerow(COLUMNS)

    try:
        sock.connect((IP_ADDRESS, PORT))
        print(f"Connected to {IP_ADDRESS}")
        eel.update_status("Connected", "green")
    except Exception as e:
        print(f"Connection failed: {e}")
        eel.update_status(f"Connection Failed: {e}", "red")
        return

    data_buffer = []


    #Open CSV in append mode
    try:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            
            while True:
                try:
                    #Send sync message
                    sock.send(b"1")
                    
                    #Receive data
                    packet = sock.recv(1024)
                    
                    if not packet:
                        break # Connection broken

                    if b'\xFF\xFF\xFF\xFF' in packet:
                        print("Connection closed by ESP32")
                        eel.update_status("Closed by ESP32", "r")
                        break

                    for byte_val in packet:
                        data_buffer.append(byte_val)

                        if len(data_buffer) == TARGET_COUNT:
                            #Save to CSV
                            writer.writerow(data_buffer)
                            f.flush()
                            
                            #Update GUI
                            eel.update_sensor_data(data_buffer)
                            data_buffer.clear()

                #Exception handling
                except socket.error as e:
                    print(f"Socket error: {e}")
                    eel.update_status(f"Error: {e}", "r")
                    break
    finally:
        sock.close()
    
@eel.expose
def get_csv_data():
    try:
        # Open in read mode and return the entire string content
        with open(CSV_FILE, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    #Start data thread
    t = threading.Thread(target=background_data_collection, daemon=True)
    t.start()
 
    #init Eel
    try:
        eel.start('index.html', mode='default', size=(1000, 800), block=False)

    except (SystemExit, KeyboardInterrupt):
        print("Closing App...")
