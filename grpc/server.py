# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./imageprocess.proto

from concurrent import futures
import logging
import time
import cv2
import numpy as np

import grpc

import imageprocess_pb2
import imageprocess_pb2_grpc

count = 0
class ImageProcess(imageprocess_pb2_grpc.ImageProcessServicer):
    def ProcessImage(self, request, context):
        print("Ping")
        global count
        current_timestamp = time.time()*1000
        network_time_ms = current_timestamp - int(request.timestamp)

        # Save image
        nparr = np.fromstring(request.image, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite('test.jpg', frame)

        print('network_time_ms: {}'.format(network_time_ms))
        # Write result file
        count += 1
        # with open("result.txt", "a") as file_object:
        #     file_object.write('{},{}\n'.format(count, network_time_ms))

        return imageprocess_pb2.ImageProcessResponse(message=request.timestamp)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    imageprocess_pb2_grpc.add_ImageProcessServicer_to_server(ImageProcess(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
