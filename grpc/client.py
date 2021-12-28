from __future__ import print_function
import logging
import time
import cv2
import numpy as np

import grpc

import imageprocess_pb2
import imageprocess_pb2_grpc

img_path = "../test_img/112x112.jpg"
# img_path = "../test_img/224x224.jpg"
# img_path = "../test_img/640x640.jpg"

n_sample = 200
delay = 0.1

with open(img_path, 'rb') as f:
  img_str = f.read()

# frame = cv2.imread(img_path)
# frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
# frame = bytes(frame)

def run():
    with grpc.insecure_channel('192.168.32.104:8080') as channel:
        stub = imageprocess_pb2_grpc.ImageProcessStub(channel)
        start = time.time()
        for i in range(n_sample):
            _ = stub.ProcessImage(imageprocess_pb2.ImageProcessResquest(timestamp=str(int(time.time()*1000)), image=img_str))
            time.sleep(delay)
        print(time.time() - start)
        # with open("grpc_call_result.txt", "a") as file_object:
        #     file_object.write('sample = {}, took = {} seconds\n'.format(n_sample, time.time() - start))
if __name__ == '__main__':
    logging.basicConfig()
    run()
