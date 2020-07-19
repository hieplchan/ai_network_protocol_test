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

n_sample = 20
delay = 0.5

frame = cv2.imread(img_path)
frame = cv2.cvtColor( frame, cv2.COLOR_RGB2GRAY )
frame = bytes(frame)
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imageprocess_pb2_grpc.ImageProcessStub(channel)
        for i in range(n_sample):
            response = stub.ProcessImage(imageprocess_pb2.ImageProcessResquest(timestamp=str(int(time.time()*1000)), image=frame))
            print("Response: " + response.message)
            time.sleep(delay)

if __name__ == '__main__':
    logging.basicConfig()
    run()
