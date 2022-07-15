import json
from server import server
from flask import request
from service.PagamentoService import *
from model.Pagamento import Pagamento
from model.Pedido import *

app = server.app
service = PagamentoService()

@app.route('/pagamento', methods=['POST'])
def insertPagamento():
    jsonPagamento = request.get_json()
    dataPagamento = jsonPagamento['dataPagamento']
    pedido = Pedido(**jsonPagamento['pedido'])
    pagamento = Pagamento(None,pedido,dataPagamento)
    
    service.insert(pagamento)
    return ''

@app.route('/pagamento', methods=['GET'])
def findAllPagamento():
    return json.dumps(service.findAll())

@app.route('/pagamento/<id>', methods=['GET'])
def findByIdPagamento(id):
    return json.dumps(service.findById(id))