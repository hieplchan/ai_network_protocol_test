import requests
import json
import time
import base64

url = 'http://0.0.0.0:8080/protocol_test/'
n_sample = 200
delay = 0.1
# img_path = "../test_img/112x112.jpg"
# img_path = "../test_img/224x224.jpg"
img_path = "./test_img/640x640.jpg"

with open(img_path, "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode('utf-8')

start = time.time()
for i in range(n_sample):
    payload = {'timestamp': int(time.time()*1000), 'image': base64_image}
    r = requests.post(url, json=payload)
    # print('n_times: {} - code: {} - body: {}'.format(i, r.status_code, r.text))
    time.sleep(delay)
    
print(time.time() - start)
with open("restful_call_result.txt", "a") as file_object:
    file_object.write('sample = {}, took = {} seconds\n'.format(n_sample, time.time() - start))
