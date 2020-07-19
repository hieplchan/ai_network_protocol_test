import requests
import json
import time
import base64

url = 'http://52.221.248.198:8080/protocol_test/'
n_sample = 20
delay = 0.1

with open("./../../test_img/640x640.jpg", "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode('utf-8')

start = time.time()
for i in range(n_sample):
    payload = {'timestamp': int(time.time()*1000), 'image': base64_image}
    r = requests.post(url, json=payload)
    print('n_times: {} - code: {} - body: {}'.format(i, r.status_code, r.text))
stop = time.time()
print(stop - start)
