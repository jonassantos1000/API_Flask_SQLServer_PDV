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
    produto = popularObjeto(jsonProduto)
    service.insert(produto)
    return '', 201

@app.route('/produto/<id>', methods=['GET'])
def findByIdProduto(id):
    produto = service.findById(id)
    return json.dumps(produto)

@app.route('/produto/<id>', methods=['PUT'])
def updateProduto(id):
    jsonProduto=request.get_json()
    produto = popularObjeto(jsonProduto)
    service.update(id,produto)
    return '', 200

@app.route('/produto/<id>', methods=['DELETE'])
def deleteProduto(id):
    service.delete(id)
    return '', 204

def popularObjeto(json):
    try:
        jsonProduto=request.get_json()
        descricao = jsonProduto['descricao']
        preco = jsonProduto['preco']
        return Produto(id,descricao,preco)
    except KeyError as error:
        raise IllegalArgument('JSON INVALIDO', f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')
