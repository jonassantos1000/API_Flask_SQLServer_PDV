import datetime
from functools import wraps
from service.PedidoService import *
from flask import request, jsonify
from model.Pedido import *
from model.Pagamento import *

service = PedidoService()

def checar_pagamento(f):
    wraps(f)
    def validacoes(*args, **kwargs):
        json = request.get_json()
        try:
            pagamento= __populaObjeto(json)
            pedido = pagamento['pedido']
            cliente = pagamento['pedido']['cliente']
            itens = pagamento['pedido']['itensPedido']
            dataPagamento = datetime.datetime.strptime(json.get("dataPagamento"), "%Y-%m-%d")
            dataVenda= datetime.datetime.strptime(pedido["dataVenda"], "%Y-%m-%d")

            #valida se o pedido id do pedido é valido
            if pedido['id'] == None or pedido['id']=="":
                response = {"Error": "Falha na requisição",
                            "Motivo": f"O campo id de pedido esta em branco ou não existe"}
                return jsonify(response), 400

            #Valida as informações do cliente
            for chave in cliente:
                if cliente[chave] == "" or cliente[chave] ==None:
                    response = {"Error": "Falha na requisição",
                                "Motivo": f"O campo '{chave}' de cliente esta em branco ou não existe"}
                    return jsonify(response), 400

            #Valida as informações se é um item de pedido valido
            if not itens:
                response = {"Error": "Falha na requisição",
                            "Motivo": f"O campo itensPedido esta em branco ou não existe"}
                return jsonify(response), 400

            #Valida as informações dos itens do pedido
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

            #valida data de pagamento
            if json.get("dataPagamento") == "" or json.get("dataPagamento") == None:
                response = {"Pagamento": "Reprovado",
                "motivo":"Data informada é invalida"}
                return jsonify(response), 400

            #valida se a data de pagamento é menor que a data de venda
            if dataPagamento < dataVenda:
                response = {"Pagamento": "Reprovado",
                "motivo":"Data de pagamento não pode ser menor que a data de venda"}
                return jsonify(response), 400

            return f(*args, **kwargs)
        except KeyError as error:
            raise IllegalArgument('JSON INVALIDO',
                                  f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')

    return(validacoes)

def __populaObjeto(json):
    valorTotal = json['pedido']['valorTotal']
    dataVenda = json['pedido']['dataVenda']
    cliente = Cliente(**json['pedido']['cliente']).dict()
    listItens = []
    for itens in json['pedido']['itensPedido']:
        produto = Produto(**itens['produto'])
        quantidade = itens['quantidade']
        precoUnitario = itens['precoUnitario']
        total = itens['total']
        item = ItensPedido(0, produto, quantidade, precoUnitario, total).dict()
        listItens.append(item)
    pedido=Pedido(json['pedido']['id'], cliente, valorTotal, dataVenda, {}, listItens).dict()

    return Pagamento(None,pedido,json['dataPagamento']).dict()

