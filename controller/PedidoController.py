from flask import request
from server import server
from service.PedidoService import PedidoService
import json

app = server.app
service = PedidoService()


@app.route('/pedido', methods=['POST'])
def insertPedido():
    jsonPedido = request.get_json()
    service.insert(jsonPedido)
    return '', 201

@app.route('/pedido/<id>', methods=['GET'])
def findByIdPedido(id):
    return json.dumps(service.findById(id))