import json
from exception.exceptionHandler import IllegalArgument
from flask import request
from service.ClienteService import *
from model.Cliente import Cliente
from server import server
from validators.clienteValidator import *

service = ClienteService()
app = server.app


@app.route('/cliente/<id>', methods=['GET'])
def findById(id):
    validaID(id)
    cliente = service.findById(id)
    response = app.response_class(
        response=json.dumps(cliente),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/cliente', methods=['GET'])
def findAll():
    list = service.findAll()
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
    return '', 201


@app.route('/cliente/<id>', methods=['DELETE'])
def delete(id):
    validaID(id)
    service.delete(id)
    return '', 204


@app.route('/cliente/<id>', methods=['PUT'], endpoint='update')
@checar_cliente
def update(id):
    validaID(id)
    jsonClient = request.get_json()
    cliente = popularObjeto(jsonClient)
    service.update(id, cliente)
    return ''


def popularObjeto(jsonClient):
    nome = jsonClient['nome']
    endereco = jsonClient['endereco']
    telefone = jsonClient['telefone']
    return Cliente(None, nome, endereco, telefone)

def validaID(id):
    if id.isdigit():
        return
    raise IllegalArgument('ID Invalido', 'O ID deve conter apenas numeros')