import requests
import json
import time
import base64

# url = 'http://52.221.248.198:8080/protocol_test/'
url = 'http://hieplc.tk:8080/protocol_test/'
n_sample = 100
delay = 0.3

time_upload = []
time_process = []
time_download = []
time_total = []

def average(time_series):
    return int(sum(time_series)/len(time_series))

with open("../test_img/112x112.jpg", "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode('utf-8')

for i in range(n_sample):
    payload = {'timestamp': int(time.time()*1000), 'image': base64_image}
    r = requests.post(url, json=payload)

    timestamp_client_receive = int(time.time()*1000)
    timestamp_client_send = int(r.json()['timestamp_client_send'])
    timestamp_server_receive = int(r.json()['timestamp_server_receive'])
    timestamp_server_processing_done = int(r.json()['timestamp_server_processing_done'])

    time_upload.append(timestamp_server_receive - timestamp_client_send)
    time_process.append(timestamp_server_processing_done - timestamp_server_receive)
    time_download.append(timestamp_client_receive - timestamp_server_processing_done)
    time_total.append(timestamp_client_receive - timestamp_client_send)

    print()

    print('Upload time: {} - Processing time: {} - Download time: {} - Total time: {}'
            .format(time_upload[-1], time_process[-1], time_download[-1], time_total[-1]))

    print('Upload time avg: {} - Processing time avg: {} - Download time avg: {} - Total time avg: {}'
            .format(average(time_upload), average(time_process), average(time_download), average(time_total)))
