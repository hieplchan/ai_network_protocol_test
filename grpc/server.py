# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./imageprocess.proto

from concurrent import futures
import logging
import time

import grpc

import imageprocess_pb2
import imageprocess_pb2_grpc

count = 0
class ImageProcess(imageprocess_pb2_grpc.ImageProcessServicer):
    def ProcessImage(self, request, context):
        global count
        current_timestamp = time.time()*1000
        network_time_ms = current_timestamp - int(request.timestamp)
        print('network_time_ms: {}'.format(network_time_ms))
        # Write result file
        count += 1
        with open("result.txt", "a") as file_object:
            file_object.write('{},{}\n'.format(count, network_time_ms))

        return imageprocess_pb2.ImageProcessResponse(message='Receive')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imageprocess_pb2_grpc.add_ImageProcessServicer_to_server(ImageProcess(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
