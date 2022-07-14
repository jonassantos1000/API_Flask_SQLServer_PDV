class Pedido:
    def __init__(self, id, cliente, valorTotal, dataVenda):
        self._id = id
        self._cliente= cliente
        self._valorTotal= valorTotal
        self._dataVenda= dataVenda

    @property
    def id (self):
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def valorTotal(self):
        return self._valorTotal

    @property
    def dataVenda(self):
        return self._dataVenda

    def dict(self):
        pedido={}
        for key in self.__dict__:
            pedido[key.replace('_','')] = self.__dict__.__getitem__(key)
        return pedido