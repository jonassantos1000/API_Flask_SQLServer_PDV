class Cliente:
    def __init__(self, id=None, nome=None, endereco=None, telefone=None):
        self._id = id
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefone

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def endereco(self):
        return self._endereco

    @property
    def telefone(self):
        return self._telefone

    def dict(self):
        client={}
        for key in self.__dict__:
            client[key.replace('_','')] = self.__dict__.__getitem__(key)
        return client