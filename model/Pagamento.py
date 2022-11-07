from model.Pedido import *

class Pagamento:
    def __init__(self, id=None, pedido=None, dataPagamento=None):
        self._id = id
        self._pedido= pedido
        self._data_pagamento = dataPagamento

    @property
    def id(self):
        return self._id

    @property
    def pedido(self):
        return self._pedido

    @property
    def data_pagamento(self):
        return self._data_pagamento

    def dict(self):
        pagamento={}
        for key in self.__dict__:
            pagamento[key[1:]] = self.__dict__.__getitem__(key)
        return pagamento