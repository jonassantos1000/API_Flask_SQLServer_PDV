import json
from exception.ExceptionHandler import IllegalArgument
from flask import request
from service.ClienteService import *
from model.Cliente import Cliente
from server import server
from validator.ClienteValidator import *
from flask_expects_json import expects_json

service = ClienteService()
app = server.app

@app.route('/cliente/<int:id>', methods=['GET'])
def findById(id):
    cliente = service.find_by_id(id)
    response = app.response_class(
        response=json.dumps(cliente),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/cliente', methods=['GET'])
def findAll():
    list = service.find_all()
    response = app.response_class(
        response=json.dumps(list),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/cliente', methods=['POST'], endpoint='insertCliente')
@checar_cliente
def insertCliente():
    jsonClient = request.get_json()
    cliente = popularObjeto(jsonClient)
    service.insert(cliente)
    response = app.response_class(
        response='',
        status=201,
        mimetype='application/json'
    )
    return response

@app.route('/cliente/<int:id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return '', 204

@app.route('/cliente/<int:id>', methods=['PUT'], endpoint='update')
@checar_cliente
def update(id):
    jsonClient = request.get_json()
    cliente = popularObjeto(jsonClient)
    service.update(id, cliente)
    return '', 200

def popularObjeto(jsonClient):
    nome = jsonClient['nome']
    endereco = jsonClient['endereco']
    telefone = jsonClient['telefone']
    email = jsonClient['email']
    return Cliente(None, nome, endereco, telefone, email)
