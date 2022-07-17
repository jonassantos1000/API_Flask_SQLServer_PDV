import json
from flask import request
from service.ClienteService import *
from model.Cliente import Cliente
from server import server

service = ClienteService()
app = server.app


@app.route('/cliente/<id>', methods=['GET'])
def findById(id):
    cliente = service.findById(id)
    return json.dumps(cliente)


@app.route('/cliente', methods=['GET'])
def findAll():
    list = service.findAll()
    return json.dumps(list)


@app.route('/cliente', methods=['POST'])
def insert():
    jsonClient = request.get_json()
    cliente = popularObjeto(jsonClient)
    service.insert(cliente)
    return '', 201


@app.route('/cliente/<id>', methods=['DELETE'])
def delete(id):
    service.delete(id)
    return '', 204


@app.route('/cliente/<id>', methods=['PUT'])
def update(id):
    jsonClient = request.get_json()
    cliente = popularObjeto(jsonClient)
    service.update(id, cliente)
    return ''


def popularObjeto(jsonClient):
    try:
        nome = jsonClient['nome']
        endereco = jsonClient['endereco']
        telefone = jsonClient['telefone']
        return Cliente(None, nome, endereco, telefone)
    except KeyError as error:
        raise IllegalArgument('JSON INVALIDO',
                              f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')
