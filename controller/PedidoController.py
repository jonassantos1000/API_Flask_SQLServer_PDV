from flask import request
from server import server
from model.Pedido import Pedido
from model.Cliente import Cliente
from model.ItensPedido import *
from service.PedidoService import PedidoService
from validator.PedidoValidators import *
import json

app = server.app
service = PedidoService()


@app.route('/pedido', methods=['GET'])
def find_all_pedido():
    list = service.find_all()
    response = app.response_class(
        response=json.dumps(list),
        status=200,
        mimetype='*application/json'
    )
    return response

@app.route('/pedido', methods=['POST'], endpoint='insert_pedido')
@checar_pedido
def insert_pedido():
    jsonPedido = request.get_json()
    pedido = __popularObjeto(jsonPedido)
    service.insert(pedido)
    return '', 201


@app.route('/pedido/<id>', methods=['PUT'], endpoint='update_pedido')
@checar_pedido
def update_pedido(id):
    jsonPedido = request.get_json()
    pedido = __popularObjeto(jsonPedido)
    service.update(id, pedido)
    return '', 200


@app.route('/pedido/<id>', methods=['GET'])
def find_by_id_pedido(id):
    response = app.response_class(
        response=json.dumps(service.find_by_id(id)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pedido/cliente/<id>', methods=['GET'])
def find_pedido_by_id_cliente(id):
    response = app.response_class(
        response=json.dumps(service.find_by_id_cliente(id)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pedido/<id>', methods=['DELETE'])
def delete_pedido(id):
    service.delete(id)
    return '', 204


def __popularObjeto(jsonPedido):
    valorTotal = jsonPedido['valor_total']
    dataVenda = jsonPedido['data_venda']
    cliente = Cliente(**jsonPedido['cliente'])
    listItens = []
    for itens in jsonPedido['itens_pedido']:
        produto = Produto(**itens['produto'])
        quantidade = itens['quantidade']
        precoUnitario = itens['preco_unitario']
        total = itens['total']
        item = ItensPedido(None, produto, quantidade, precoUnitario, total)
        listItens.append(item)
    return Pedido(None, cliente, valorTotal, dataVenda, {}, listItens)
