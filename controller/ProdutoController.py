import json
from flask import request
from service.ProdutoService import *
from model.Produto import *
from server import server
from validator.produtoValidators import *

service = ProdutoService()
app = server.app


@app.route('/produto', methods=['GET'])
def findAllProduto():
    list = service.findAll()
    response = app.response_class(
        response=json.dumps(list),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/produto', methods=['POST'], endpoint='insertProduto')
@checar_produto
def insertProduto():
    jsonProduto = request.get_json()
    produto = popularObjeto(jsonProduto)
    service.insert(produto)
    return '', 201


@app.route('/produto/<id>', methods=['GET'])
def findByIdProduto(id):
    produto = service.findById(id)
    response = app.response_class(
        response=json.dumps(produto),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/produto/<id>', methods=['PUT'], endpoint='updateProduto')
@checar_produto
def updateProduto(id):
    jsonProduto = request.get_json()
    produto = popularObjeto(jsonProduto)
    service.update(id, produto)
    return '', 200


@app.route('/produto/<id>', methods=['DELETE'])
def deleteProduto(id):
    service.delete(id)
    return '', 204


def popularObjeto(json):
    jsonProduto = request.get_json()
    descricao = jsonProduto['descricao']
    preco = jsonProduto['preco']
    return Produto(id, descricao, preco)
