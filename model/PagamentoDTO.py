class PagamentoDTO:
    def __init__(self, id, dataPagamento, status=None):
        self._id = id
        self._data_pagamento = dataPagamento
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def data_pagamento(self):
        return self._data_pagamento

    @property
    def status(self):
        return self._status

    def dict(self):
        pagamento={}
        for key in self.__dict__:
            pagamento[key[1:]] = self.__dict__.__getitem__(key)
        return pagamento