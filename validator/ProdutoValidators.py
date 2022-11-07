from functools import wraps
from service.PedidoService import *
from flask import request, jsonify


def checar_produto(f):
    wraps(f)

    def validacoesProduto(*args, **kwargs):
        json = request.get_json()

        # Valida se os campos do json são diferentes de branco e null
        try:
            for elemento in json:
                valor = json[elemento]
                if valor == "" or valor == None:
                    response = {"Error": "Argumento Invalido",
                                "Motivo": f"O campo '{elemento}' esta em branco ou não existe"}
                    return jsonify(response), 400

            if json["preco"] <= 0:
                response = {"Error": "Argumento Invalido",
                            "Motivo": f"O campo 'preco' deve ser maior que zero"}
                return jsonify(response), 400

            return f(*args, **kwargs)
        except KeyError as error:
            raise IllegalArgument('JSON INVALIDO',
                                  f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')

    return (validacoesProduto)
