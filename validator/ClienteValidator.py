from functools import wraps
from flask import request, jsonify
from exception.ExceptionHandler import *


def checar_cliente(f):
    wraps(f)

    def validacoesCliente(*args, **kwargs):
        json = request.get_json()

        # Valida se os campos do json são diferentes de branco e null
        try:
            for elemento in json:
                valor = json[elemento]
                if not valor:
                    response = {"Error": "Falha na requisição",
                                "Motivo": f"O campo '{elemento}' esta em branco ou não existe"}
                    return jsonify(response), 400
            return f(*args, **kwargs)
        except KeyError as error:
            raise IllegalArgument('JSON INVALIDO',
                                  f'O JSON INFORMADO NÃO TEM O CAMPO {error.__str__()}, POR FAVOR REALIZE O AJUSTE E TENTE NOVAMENTE !')

    return(validacoesCliente)