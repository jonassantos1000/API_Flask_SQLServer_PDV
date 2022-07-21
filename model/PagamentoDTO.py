class PagamentoDTO:
    def __init__(self, id, dataPagamento, status=None):
        self._id = id
        self._dataPagamento = dataPagamento
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def dataPagamento(self):
        return self._dataPagamento

    @property
    def status(self):
        return self._status

    def dict(self):
        pagamento={}
        for key in self.__dict__:
            pagamento[key.replace('_','')] = self.__dict__.__getitem__(key)
        return pagamento