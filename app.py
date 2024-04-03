from flask import Flask, request

app = Flask(__name__)

@app.route('/get', methods=['POST'])
def echo_string():
        return '1234'

