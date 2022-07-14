import json
from flask import request
from service.ProdutoService import *
from model.Produto import *
from server import server

service = ProdutoService()
app = server.app


@app.route('/produto', methods=['GET'])
def findAllProduto():
    list = service.findAll()
    return json.dumps(list)

@app.route('/produto/<id>', methods=['GET'])
def findByIdProduto(id):
    produto = service.findById(id)
    return json.dumps(produto)

@app.route('/produto/<id>', methods=['POST'])
def updateProduto(id):
    
    produto = service.findById(id)
    return json.dumps(produto)

