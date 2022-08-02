import cv2
import io
import socket
import struct
import time
import pickle
import zlib

# HOST='0.0.0.0'
HOST='hieplc.tk'
# PORT_IMAGE=8080
# PORT_DATA=8081
PORT_IMAGE=8082
PORT_DATA=8083

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT_DATA))

time_upload = []
time_process = []
time_download = []
time_total = []

def average(time_series):
    return int(sum(time_series)/len(time_series))

data = b""
while True:
    while len(data) < 39:
        data += client_socket.recv(13)
        if not data:
            client_socket.close()
            break

    timestamp_client_receive = int(time.time()*1000)
    timestamp_client_send = int(data[:13])
    timestamp_server_receive = int(data[13:26])
    timestamp_server_processing_done = int(data[26:])

    time_upload.append(timestamp_server_receive - timestamp_client_send)
    time_process.append(timestamp_server_processing_done - timestamp_server_receive)
    time_download.append(timestamp_client_receive - timestamp_server_processing_done)
    time_total.append(timestamp_client_receive - timestamp_client_send)

    print()

    print('Upload time: {} - Processing time: {} - Download time: {} - Total time: {}'
            .format(time_upload[-1], time_process[-1], time_download[-1], time_total[-1]))

    print('Upload time avg: {} - Processing time avg: {} - Download time avg: {} - Total time avg: {}'
            .format(average(time_upload), average(time_process), average(time_download), average(time_total)))

    data = data[46:]
