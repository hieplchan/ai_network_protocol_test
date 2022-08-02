# sudo timedatectl set-ntp off
# sudo timedatectl set-ntp on

from flask_api import FlaskAPI
from flask import request
import time
from flask import session, g

app = FlaskAPI(__name__)
count = 0

upload_time_ms = []

@app.route('/protocol_test/', methods=['POST'])
def protocol_test():
    global count
    current_timestamp = time.time()*1000
    request_json = request.get_json()

    timestamp = request_json['timestamp']
    # image = request_json['image']

    network_time_ms = current_timestamp - timestamp
    print('network_time_ms: {}'.format(network_time_ms))

    # Write result file
    count += 1
    with open("test4_112.csv", "a") as file_object:
        file_object.write('{},{}\n'.format(count, network_time_ms))

    # Average time
    upload_time_ms.append(network_time_ms)
    print('Average time: {}'.format(sum(upload_time_ms)/len(upload_time_ms)))

    return {
        "message": "Receive"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
