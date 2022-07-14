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

@app.route('/produto', methods=['POST'])
def insertProduto():
    jsonProduto=request.get_json()
    id = jsonProduto['id']
    descricao = jsonProduto['descricao']
    preco = jsonProduto['preco']
    produto = Produto(id,descricao,preco)
    service.insert(produto)
    return '', 201

@app.route('/produto/<id>', methods=['GET'])
def findByIdProduto(id):
    produto = service.findById(id)
    return json.dumps(produto)

@app.route('/produto/<id>', methods=['PUT'])
def updateProduto(id):
    jsonProduto=request.get_json()
    descricao = jsonProduto['descricao']
    preco = jsonProduto['preco']
    produto = Produto(descricao=descricao,preco=preco)
    service.update(id,produto)
    return '', 200

@app.route('/produto/<id>', methods=['DELETE'])
def deleteProduto(id):
    service.delete(id)
    return '', 204

