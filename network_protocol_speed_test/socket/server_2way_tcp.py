# sudo timedatectl set-ntp off
# sudo timedatectl set-ntp on

import socket
import sys
import pickle
import cv2
import numpy as np
import struct ## new
import zlib
import time

HOST='0.0.0.0'
# PORT_IMAGE=8080
# PORT_DATA=8081
PORT_IMAGE=8082
PORT_DATA=8083

socket_data = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_data.bind((HOST,PORT_DATA))
socket_data.listen(10)
socket_data_conn, socket_data_addr = socket_data.accept()
print('socket_data_conn is listening')

socket_image = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_image.bind((HOST,PORT_IMAGE))
socket_image.listen(10)
socket_image_conn, socket_image_addr = socket_image.accept()
print('socket_image_conn is listening')

payload_size = 4
# msg_size = 3790
# msg_size = 9824
msg_size = 47684

total_size = payload_size + msg_size

def simulate_workload():
    time.sleep(0.1)

data = b""
count = 0
while True:
    # Data receive
    while len(data) < total_size:
        data += socket_image_conn.recv(10)
    timestamp_client_send = int(data[4:17].decode('utf-8'))

    # Get timestamp
    timestamp_server_receive = time.time()*1000

    # Decode data to image
    frame_data = data[17:total_size]
    frame = zlib.decompress(frame_data)
    frame = cv2.imdecode(np.frombuffer(frame, dtype=np.int8), cv2.IMREAD_COLOR)

    # cv2.imwrite('./' + str(count) + '.jpg', frame)
    # cv2.imshow('ImageWindow',frame)
    # cv2.waitKey(1)

    # Heavy workload
    # simulate_workload()

    timestamp_server_processing_done = time.time()*1000

    # Send data to client
    test_data = bytes(str(int(timestamp_client_send)), 'utf-8') \
                + bytes(str(int(timestamp_server_receive)), 'utf-8') \
                + bytes(str(int(timestamp_server_processing_done)), 'utf-8')

    socket_data_conn.send(test_data)

    # Others
    data = data[total_size:]
    if (count == 99):
        break

socket_data.close()
socket_image.close()
