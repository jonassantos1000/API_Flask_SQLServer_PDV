import json
from flask import request
from service.ProdutoService import *
from model.Produto import *
from server import server
from validator.ProdutoValidators import *

service = ProdutoService()
app = server.app


@app.route('/produto', methods=['GET'])
def find_all_produto():
    list = service.find_all()
    response = app.response_class(
        response=json.dumps(list),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/produto', methods=['POST'], endpoint='insert_produto')
@checar_produto
def insert_produto():
    jsonProduto = request.get_json()
    produto = popularObjeto(jsonProduto)
    service.insert(produto)
    return '', 201


@app.route('/produto/<id>', methods=['GET'])
def find_by_id_produto(id):
    produto = service.find_by_id(id)
    response = app.response_class(
        response=json.dumps(produto),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/produto/<id>', methods=['PUT'], endpoint='update_produto')
@checar_produto
def update_produto(id):
    jsonProduto = request.get_json()
    produto = popularObjeto(jsonProduto)
    service.update(id, produto)
    return '', 200


@app.route('/produto/<id>', methods=['DELETE'])
def delete_produto(id):
    service.delete(id)
    return '', 204


def popularObjeto(json):
    jsonProduto = request.get_json()
    descricao = jsonProduto['descricao']
    preco = jsonProduto['preco']
    return Produto(id, descricao, preco)
