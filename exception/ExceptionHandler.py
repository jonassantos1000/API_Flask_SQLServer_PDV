import json

from flask import jsonify, make_response, render_template
from jsonschema.exceptions import ValidationError

from exception import EmptyProductList
from exception.IllegalArgument import *
from exception.IntegrityError import *
from exception.BadRequest import *
from exception.EmptyProductList import *
from exception.NotFound import *
from server import server
from werkzeug.exceptions import HTTPException

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

@app.errorhandler(EmptyProductList)
def handle_bad_request(err):
    response = {"error": err.description, "message": err.args[1]}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(NotFound)
def handle_not_found(err):
    response = {"error": err.description, "message": err.args[1]}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(404)
def handle_method_not_allowed(err):
    response = {"error": "NOT FOUND", "message": "NÃO FOI POSSIVEL ENCONTRAR UM RECURSO VÁLIDO PARA ESTE ENDPOINT"}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(405)
def handle_method_not_allowed(err):
    response = {"error": "METHOD NOT ALLOWED", "message": "ESTE ENDPOINT NÃO POSSUI FUNCIONALIDADE PARA ESTA OPERAÇÃO"}
    app.logger.error
    return jsonify(response), err.code

@app.errorhandler(500)
def handle_method_not_allowed(err):
    response = {"error": "FALHA NA REQUISIÇÃO", "message": "OCORREU UM ERRO DURANTE A REQUISIÇÃO"}
    app.logger.error
    return jsonify(response), 400