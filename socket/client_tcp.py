import cv2
import io
import socket
import struct
import time
import pickle
import zlib

n_sample = 100
delay = 0.1

# img_path = "../test_img/112x112.jpg"
# size = 3790

# img_path = "../test_img/224x224.jpg"
# size = 9824

img_path = "../test_img/640x640.jpg"
size = 47684

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('52.221.248.198', 8080))
# client_socket.connect(('localhost', 8080))
connection = client_socket.makefile('wb')

img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

start = time.time()
for i in range(n_sample):
    frame = cv2.imread(img_path)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    zip_data = zlib.compress(frame)
    data = bytes(str(int(time.time()*1000)), 'utf-8') + zip_data
    client_socket.sendall(struct.pack(">L", size) + data)
    print("{}: {}".format(img_counter, size))
    img_counter += 1
    # time.sleep(delay)
stop = time.time()
print(stop - start)
