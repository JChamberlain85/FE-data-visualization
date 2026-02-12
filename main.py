import socket

sock = socket.socket()

ip = "192.168.4.1"
port = 80

sock.connect((ip, port))
print(f"Connected to {ip}")

data_buffer = []
target_count = 71 # 0 to 70 is 71 numbers

while True:
    #Send connection message to esp
    sock.send(b"1") 
    packet = sock.recv(1024) 
    
    if not packet:
        print("Connection closed by ESP32")
        break

    for byte_val in packet:
        data_buffer.append(byte_val)

        # Full set check
        if len(data_buffer) == target_count:
            print(f"{data_buffer}")

            # Reset
            data_buffer.clear()