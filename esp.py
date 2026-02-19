import socket
import pandas as pd
import time

sock = socket.socket()

ip = "192.168.4.1"
port = 80

sock.connect((ip, port))
print(f"Connected to {ip}")

data_buffer = []
target_count = 71 # 0 to 70 is 71 numbers

# Receives data from the esp32 and appends the data to a csv file
def receive_data():
    while True:
        # Send connection message to esp32
        time.sleep(0.5)
        sock.send(b"1") 
        packet = sock.recv(1024) 

        if packet == 'f':
            print('Connection closed by ESP32')
            break

        for byte_val in packet:
            data_buffer.append(byte_val)

            # Full set check
            if len(data_buffer) == target_count:
                df = pd.read_csv('fe_sample.csv')  # Fetch latest price
                df.loc[-1] = data_buffer

                # Reset
                data_buffer.clear()
