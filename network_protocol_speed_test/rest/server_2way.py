# sudo timedatectl set-ntp off
# sudo timedatectl set-ntp on

from flask_api import FlaskAPI
from flask import request
import time
from flask import session, g
import cv2
import base64
from PIL import Image
import io

app = FlaskAPI(__name__)
count = 0

def simulate_workload():
    time.sleep(0.1)

@app.route('/protocol_test/', methods=['POST'])
def protocol_test():
    global count

    timestamp_client_send = request.data['timestamp']
    timestamp_server_receive = time.time()*1000

    # Decode data to image
    image = request.data['image']
    img = Image.open(io.BytesIO(base64.b64decode(image)))

    # Heavy workload
    # simulate_workload()

    timestamp_server_processing_done = time.time()*1000

    return {
        "timestamp_client_send": timestamp_client_send,
        "timestamp_server_receive": timestamp_server_receive,
        "timestamp_server_processing_done": timestamp_server_processing_done
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
