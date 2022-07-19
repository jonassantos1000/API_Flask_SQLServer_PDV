from functools import wraps
from flask import request, jsonify
from exception.exceptionHandler import *
from model.Cliente import Cliente
from model.ItensPedido import ItensPedido
from model.Pedido import Pedido
from model.Produto import Produto


def checar_pedido(f):
    wraps(f)

    def validacoesPedido(*args, **kwargs):
        try:
            json = request.get_json()
            pedido= __populaObjeto(json).dict()
            cliente= pedido['cliente']
            itens = pedido['itensPedido']

            for chave in cliente:
                if cliente[chave] == "" or cliente[chave] ==None:
                    response = {"Error": "Falha na requisição",
                                "Motivo": f"O campo '{chave}' de cliente esta em branco ou não existe"}
                    return jsonify(response), 400

            for item in itens:
                for chave in item:
                    if item[chave] == "" or item[chave] ==None:
                        response = {"Error": "Falha na requisição",
                                    "Motivo": f"O campo '{chave}' do {item} esta em branco ou não existe"}
                        return jsonify(response), 400
                    if chave == 'produto':
                        produtos = item[chave].dict()
                        for subChave in produtos:
                            if produtos[subChave] == "" or produtos[subChave] == None:
                                response = {"Error": "Falha na requisição",
                                            "Motivo": f"O campoo '{subChave}' do {chave} esta em branco ou não existe"}
                                return jsonify(response), 400

            return f(*args, **kwargs)

        except KeyError as error:
            raise IllegalArgument('JSON INVALIDO',
                              f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')

    return (validacoesPedido)

def __populaObjeto(jsonPedido):
    valorTotal = jsonPedido['valorTotal']
    dataVenda = jsonPedido['dataVenda']
    cliente = Cliente(**jsonPedido['cliente']).dict()
    listItens = []
    for itens in jsonPedido['itensPedido']:
        produto = Produto(**itens['produto'])
        quantidade = itens['quantidade']
        precoUnitario = itens['precoUnitario']
        total = itens['total']
        item = ItensPedido(0, produto, quantidade, precoUnitario, total).dict()
        listItens.append(item)
    return Pedido(None, cliente, valorTotal, dataVenda, {}, listItens)


