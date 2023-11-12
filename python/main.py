import datetime
import os
from urllib.parse import urljoin

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def resp_main():
    data = request.json

    if requests.get(os.environ['LIMITER_URL'], json=data).ok:
        response = requests.get(os.environ['NODE_URl'])
        return f"Python pod: {os.environ['POD_NAME']}, Time: {datetime.datetime.now().isoformat()}\n{response.text}", 200
    return '', 429


@app.route('/register')
def register():
    data = request.json
    response = requests.get(urljoin(os.environ['LIMITER_URL'], '/register'), json=data)
    return response.text, response.status_code


@app.route('/params')
def configure_limiter():
    data = request.json
    response = requests.get(urljoin(os.environ['LIMITER_URL'], '/params'), json=data)
    return response.text, response.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
