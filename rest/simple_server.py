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
    # print(request.headers)

    file = request.files['image']
    file_name = file.filename
    print(file_name)

    bbox_json = request.values['bbox_json']
    print(bbox_json)

    # file.save(file_name)

    return {
        "message": "Receive"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
