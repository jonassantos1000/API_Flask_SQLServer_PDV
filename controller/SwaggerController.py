import os
from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from server import server


app = server.app

SWAGGER_URL = '/swagger'
API_URL = '/config/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PDV"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route("/config/swagger.json")
def specs():
    return send_from_directory(os.getcwd(), "config/swagger.json")