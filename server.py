import os

from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint


class Server():
    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        self.app.run(debug=True)


server = Server()
