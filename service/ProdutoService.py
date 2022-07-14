from dao.ProdutoDAO import *

dao = ProdutoDAO()

class ProdutoService:
    def insert(self, produto):
        dao.save(produto)

    def findById(self, id):
        if self.__produtoEhValido(id):
            return dao.findById(id)

    def findAll(self):
        return dao.findAll()

    def update(self,id, produto):
        if self.__produtoEhValido(id):
            dao.update(id, produto)

    def delete(self,id):
        if self.__produtoEhValido(id):
            dao.delete(id)

    def __produtoEhValido(self,id):
        produto = dao.findById(id)
        if(produto != None):
            return True
        return False
