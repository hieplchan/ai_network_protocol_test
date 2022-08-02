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
PORT=8080

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = 4
# msg_size = 3790
# msg_size = 9824
msg_size = 47684

total_size = payload_size + msg_size

upload_time_ms = []

count = 0
while True:
    # while len(data) < payload_size:
    #     data += conn.recv(4096)
    #
    # # print("Done Recv: {}".format(len(data)))
    # packed_msg_size = data[:payload_size]
    # data = data[payload_size:]
    # msg_size = struct.unpack(">L", packed_msg_size)[0]
    # print("msg_size: {}".format(msg_size))

    while len(data) < total_size:
        data += conn.recv(10)
    current_timestamp = time.time()*1000

    # Time stamp
    timestamp = int(data[4:17].decode('utf-8'))
    network_time_ms = current_timestamp - timestamp
    upload_time_ms.append(network_time_ms)
    print('network_time_ms: {}'.format(network_time_ms))
    # Write result file
    count += 1
    with open("test4_640_asdad.csv", "a") as file_object:
        file_object.write('{},{}\n'.format(count, network_time_ms))

    # Image
    frame_data = data[17:total_size]
    frame = zlib.decompress(frame_data)
    frame = cv2.imdecode(np.frombuffer(frame, dtype=np.int8), cv2.IMREAD_COLOR)
    # cv2.imwrite('./' + str(count) + '.jpg', frame)
    # cv2.imshow('ImageWindow',frame)
    # cv2.waitKey(1)

    # Others
    data = data[total_size:]

    # Average time
    print('Average time: {}'.format(sum(upload_time_ms)/len(upload_time_ms)))
