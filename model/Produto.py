class Produto:
    def __init__(self, id = None, descricao = None, preco=None):
        self._id = id
        self._descricao = descricao
        self._preco = preco

    @property
    def id(self):
        return self._id

    @property
    def descricao(self):
        return self._descricao

    @property
    def preco(self):
        return self._preco

    def dict(self):
        produto={}
        for key in self.__dict__:
            produto[key.replace('_','')] = self.__dict__.__getitem__(key)
        return produto