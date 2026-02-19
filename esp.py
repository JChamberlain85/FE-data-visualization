import socket
import pandas as pd
import time
import csv

sock = socket.socket()

ip = "192.168.4.1"
port = 80

sock.connect((ip, port))
print(f"Connected to {ip}")

data_buffer = []
target_count = 71 # 0 to 70 is 71 numbers
exit = False

headers = [
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


# Receives data from the esp32 and appends the data to a csv file
#def receive_data():
with open("fe_sample.csv", mode="w", newline = '', encoding = 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    while True:
        # Send connection message to esp32
        #time.sleep(0.5)
        sock.send(b"1") 
        packet = sock.recv(1024) 

        for byte_val in packet:
            if byte_val == 'f':
                exit = 1
                break

            data_buffer.append(byte_val)

        if exit == 1:
            break

        # Full set check
        #if len(data_buffer) == target_count:

        # writes to the csv file
        writer.writerow(data_buffer)

        # Reset
        data_buffer.clear()
        
    print("File Successfully Filled")
            


#receive_data()
