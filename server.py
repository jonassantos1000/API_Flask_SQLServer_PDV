from flask import Flask, send_from_directory


class Server():
    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        self.app.run(host='0.0.0.0', threaded=True, debug=True)


server = Server()
