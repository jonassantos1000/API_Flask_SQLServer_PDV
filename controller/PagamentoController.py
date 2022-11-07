import json
from server import server
from flask import request
from service.PagamentoService import *
from model.Pagamento import Pagamento
from model.Pedido import *
from validator.PagamentoValidator import checar_pagamento

app = server.app
service = PagamentoService()


@app.route('/pagamento', methods=['POST'])
@checar_pagamento
def insert_pagamento():
    jsonPagamento = request.get_json()
    pagamento = popularObjeto(jsonPagamento)
    service.insert(pagamento)
    return '', 201


@app.route('/pagamento', methods=['GET'])
def find_all_pagamento():
    response = app.response_class(
        response=json.dumps(service.find_all()),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pagamento/<id>', methods=['GET'])
def find_by_id_pagamento(id):
    response = app.response_class(
        response=json.dumps(service.find_by_id(id)),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/pagamento/<id>', methods=['DELETE'])
def delete_pagamento(id):
    service.delete(id)
    return '', 204


def popularObjeto(jsonPagamento):
    dataPagamento = jsonPagamento['data_pagamento']
    pedido = Pedido(**jsonPagamento['pedido'])
    return Pagamento(None, pedido, dataPagamento)
