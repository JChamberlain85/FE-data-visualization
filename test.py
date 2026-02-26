import eel
import socket
import threading
import pandas as pd
import csv
import os

#CONFIG
IP_ADDRESS = "192.168.4.1"
PORT = 80
TARGET_COUNT = 71 
CSV_FILE = 'fe_sample.csv'
eel.init('web')


def get_column_names():
    try:
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE, nrows=0)
            return list(df.columns)
    except Exception as e:
        print(f"Error reading CSV headers: {e}")
    return [f"Sensor {i}" for i in range(TARGET_COUNT)]

COLUMNS = get_column_names()

def background_data_collection():
    print(f"Attempting to connect to {IP_ADDRESS}...")
    
    sock = socket.socket()
    sock.settimeout(5)

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

                    if b'f' in packet:
                        print("Connection closed by ESP32")
                        eel.update_status("Closed by ESP32", "r")
                        break

                    for byte_val in packet:
                        data_buffer.append(byte_val)

                        if len(data_buffer) == TARGET_COUNT:
                            #Save to CSV
                            writer.writerow(data_buffer)
                            
                            #Update GUI
                            eel.update_sensor_data(data_buffer)
                            
                            data_buffer.clear()

                except socket.error as e:
                    print(f"Socket error: {e}")
                    eel.update_status(f"Error: {e}", "r")
                    break
    finally:
        sock.close()

if __name__ == '__main__':
    #Start data thread
    t = threading.Thread(target=background_data_collection, daemon=True)
    t.start()
 
    #init Eel
    try:
        eel.start('index.html', mode='default', size=(1000, 800), block=False)

        while True:
            eel.sleep(1.0)
    except (SystemExit, KeyboardInterrupt):
        print("Closing App...")