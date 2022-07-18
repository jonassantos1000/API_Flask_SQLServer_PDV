import datetime
from functools import wraps
from service.PedidoService import *
from flask import request, jsonify

service = PedidoService()

def checar_pagamento(f):
    wraps(f)
    def validacoes(*args, **kwargs):
        json = request.get_json()
        try:
            if json.get("dataPagamento") == "" or json.get("dataPagamento") == None:
                response = {"Pagamento": "Reprovado",
                "motivo":"Data informada é invalida"}
                return jsonify(response), 400

            pedido = service.findById(json.get("pedido").get("id"))
            dataPagamento = datetime.datetime.strptime(json.get("dataPagamento"), "%Y-%m-%d")
            dataVenda= datetime.datetime.strptime(pedido["dataVenda"], "%Y-%m-%d")

            if dataPagamento < dataVenda:
                response = {"Pagamento": "Reprovado",
                "motivo":"Data de pagamento não pode ser menor que a data de venda"}
                return jsonify(response), 400

            return f(*args, **kwargs)
        except KeyError as error:
            raise IllegalArgument('JSON INVALIDO',
                                  f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')

    return(validacoes)