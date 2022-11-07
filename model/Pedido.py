class Pedido:
    def __init__(self, id=None, cliente=None, valor_total=None, data_venda=None, pagamento=None, itens_pedido=None):
        self._id = id
        self._cliente= cliente
        self._valor_total= valor_total
        self._data_venda= data_venda
        self._pagamento = pagamento
        self._itens_pedido = itens_pedido


    @property
    def id (self):
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def itens_pedido(self):
        return self._itens_pedido

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def data_venda(self):
        return self._data_venda

    @property
    def pagamento(self):
        return self._pagamento

    @id.setter
    def id(self, valor):
        self._id = valor

    def dict(self):
        pedido={}
        for key in self.__dict__:
            pedido[key[1:]] = self.__dict__.__getitem__(key)
        return pedido