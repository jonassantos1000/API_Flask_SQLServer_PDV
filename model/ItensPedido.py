from model.Produto import *

class ItensPedido:
    def __init__(self, id, produto, quantidade, total):
        self._id = id
        self._produto = produto
        self._quantidade = quantidade
        self._total = total

    @property
    def id(self):
        return self._id

    @property
    def produto(self):
        return self._produto

    @property
    def quantidade(self):
        return self._quantidade

    @property
    def total(self):
        return self._total

    def dict(self):
        itens={}
        for key in self.__dict__:
            itens[key.replace('_','')] = self.__dict__.__getitem__(key)
        return itens
