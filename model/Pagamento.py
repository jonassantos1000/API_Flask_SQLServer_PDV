class Pagamento:
    def __init__(self, id=None, pedido=None, dataPagamento=None):
        self._id = id
        self._pedido= pedido
        self._dataPagamento = dataPagamento

    @property
    def id(self):
        return self._id

    @property
    def pedido(self):
        return self._pedido

    @property
    def dataPagamento(self):
        return self._dataPagamento

    def dict(self):
        pagamento={}
        for key in self.__dict__:
            pagamento[key.replace('_','')] = self.__dict__.__getitem__(key)
        return pagamento