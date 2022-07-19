from functools import wraps
from flask import request, jsonify
from exception.exceptionHandler import *

def NotBlank(f):
    def validacoes(*args, **kwargs):
        if args[1] == None or args[1] == "":
            response = {"Error": "Falha na requisição",
                        "Motivo": f"O campo '{args[0].nam}' esta em branco ou não existe"}
            return jsonify(response), 400


