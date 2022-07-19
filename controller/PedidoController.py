from flask import request
from server import server
from model.Pedido import Pedido
from model.Cliente import Cliente
from model.ItensPedido import *
from service.PedidoService import PedidoService
from validators.pedidoValidators import *
import json

app = server.app
service = PedidoService()


@app.route('/pedido', methods=['GET'])
def findAllPedido():
    list = service.findAll()
    response = app.response_class(
        response=json.dumps(list),
        status=200,
        mimetype='*application/json'
    )
    return response

@app.route('/pedido', methods=['POST'], endpoint='insertPedido')
@checar_pedido
def insertPedido():
    jsonPedido = request.get_json()
    pedido = __popularObjeto(jsonPedido)
    service.insert(pedido)
    return '', 201


@app.route('/pedido/<id>', methods=['PUT'], endpoint='updatePedido')
@checar_pedido
def updatePedido(id):
    jsonPedido = request.get_json()
    pedido = __popularObjeto(jsonPedido)
    service.update(id, pedido)
    return '', 200


@app.route('/pedido/<id>', methods=['GET'])
def findByIdPedido(id):
    response = app.response_class(
        response=json.dumps(service.findById(id)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pedido/cliente/<id>', methods=['GET'])
def findPedidoByIdCliente(id):
    response = app.response_class(
        response=json.dumps(service.findByIdCliente(id)),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/pedido/<id>', methods=['DELETE'])
def deletePedido(id):
    service.delete(id)
    return '', 204


def __popularObjeto(jsonPedido):
    valorTotal = jsonPedido['valorTotal']
    dataVenda = jsonPedido['dataVenda']
    cliente = Cliente(**jsonPedido['cliente'])
    listItens = []
    for itens in jsonPedido['itensPedido']:
        produto = Produto(**itens['produto'])
        quantidade = itens['quantidade']
        precoUnitario = itens['precoUnitario']
        total = itens['total']
        item = ItensPedido(None, produto, quantidade, precoUnitario, total)
        listItens.append(item)
    return Pedido(None, cliente, valorTotal, dataVenda, {}, listItens)
