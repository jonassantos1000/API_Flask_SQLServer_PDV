from model.Produto import *

class ItensPedido:
    def __init__(self, id, produto, quantidade, precoUnitario,total):
        self._id = id
        self._produto = produto
        self._quantidade = quantidade
        self._preco_unitario= precoUnitario
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
    def preco_unitario(self):
        return self._preco_unitario

    @property
    def total(self):
        return self._total

    def dict(self):
        itens={}
        for key in self.__dict__:
            itens[key[1:]] = self.__dict__.__getitem__(key)
        return itens
