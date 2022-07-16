from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        SWAGGER_URL = '/swagger'
        API_URL = '/static/swagger.json'
        SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={
                'app_name': "Seans-Python-Flask-REST-Boilerplate"
            }
        )
        self.app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    def run(self):
        self.app.run(debug=True)


server = Server()