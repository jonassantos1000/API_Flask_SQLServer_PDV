class Cliente:
    def __init__(self, id=None, nome=None, endereco=None, telefone=None, email=None):
        self._id = id
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefone
        self._email = email

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

    @property
    def email(self):
        return self._email

    @id.setter
    def id(self, valor):
        self._id=valor

    def dict(self):
        client={}
        for key in self.__dict__:
            client[key[1:]] = self.__dict__.__getitem__(key)
        return client