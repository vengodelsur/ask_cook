# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import json
app = Flask(__name__)


@app.route("/", methods=['POST'])
def hello():
    with open('default_response.json') as f:
        default_response = json.load(f)

    return jsonify(default_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
