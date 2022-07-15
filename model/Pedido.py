class Pedido:
    def __init__(self, id, cliente, valorTotal, dataVenda, pagamento, itensPedido):
        self._id = id
        self._cliente= cliente
        self._valorTotal= valorTotal
        self._dataVenda= dataVenda
        self._pagamento = pagamento
        self._itensPedido = itensPedido


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

    @property
    def pagamento(self):
        return self._pagamento

    @property
    def itensPedido(self):
        return self._itensPedido

    def dict(self):
        pedido={}
        for key in self.__dict__:
            pedido[key.replace('_','')] = self.__dict__.__getitem__(key)
        return pedido