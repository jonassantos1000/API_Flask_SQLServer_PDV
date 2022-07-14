from flask import request
from server import server
from model.Pedido import Pedido
from model.Cliente import Cliente
from service.PedidoService import PedidoService
import json

app = server.app
service = PedidoService()

@app.route('/pedido', methods=['GET'])
def findAllPedido():
    return json.dumps(service.findAll())

@app.route('/pedido', methods=['POST'])
def insertPedido():
    jsonPedido = request.get_json()
    valorTotal = jsonPedido['valorTotal']
    dataVenda = jsonPedido['dataVenda']
    cliente = Cliente(**jsonPedido['cliente'])
    pedido = Pedido(None, cliente, valorTotal, dataVenda)
    service.insert(pedido)
    return '', 201

@app.route('/pedido/<id>', methods=['PUT'])
def updatePedido(id):
    jsonPedido = request.get_json()
    valorTotal = jsonPedido['valorTotal']
    dataVenda = jsonPedido['dataVenda']
    cliente = Cliente(**jsonPedido['cliente'])
    pedido = Pedido(None, cliente, valorTotal, dataVenda)
    service.update(id,pedido)
    return '', 200

@app.route('/pedido/<id>', methods=['GET'])
def findByIdPedido(id):
    return json.dumps(service.findById(id))

@app.route('/pedido/<id>', methods=['DELETE'])
def deletePedido(id):
    service.delete(id)
    return '', 204
