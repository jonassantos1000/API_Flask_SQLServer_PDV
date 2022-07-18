import json
from server import server
from flask import request
from service.PagamentoService import *
from model.Pagamento import Pagamento
from model.Pedido import *
from validators.pagamentoValidator import checar_pagamento

app = server.app
service = PagamentoService()


@app.route('/pagamento', methods=['POST'])
@checar_pagamento
def insertPagamento():
    jsonPagamento = request.get_json()
    pagamento = popularObjeto(jsonPagamento)
    service.insert(pagamento)
    return '', 201


@app.route('/pagamento', methods=['GET'])
def findAllPagamento():
    return json.dumps(service.findAll())


@app.route('/pagamento/<id>', methods=['GET'])
def findByIdPagamento(id):
    return json.dumps(service.findById(id))


@app.route('/pagamento/<id>', methods=['DELETE'])
def deletePagamento(id):
    service.delete(id)
    return '', 204


def popularObjeto(jsonPagamento):
    dataPagamento = jsonPagamento['dataPagamento']
    pedido = Pedido(**jsonPagamento['pedido'])
    return Pagamento(None, pedido, dataPagamento)
