from flask import jsonify, make_response

from exception.IllegalArgument import *
from exception.IntegrityError import *
from exception.BadRequest import *
from server import server

app = server.app

@app.errorhandler(IllegalArgument)
def handle_bad_request(err):
    response = {"error": err.description, "message": err.args[1]}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(IntegrityError)
def handle_bad_request(err):
    response = {"error": err.description, "message": err.args[1]}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(BadRequest)
def handle_bad_request(err):
    response = {"error": err.description, "message": err.args[1]}
    app.logger.error
    return jsonify(response), err.code

