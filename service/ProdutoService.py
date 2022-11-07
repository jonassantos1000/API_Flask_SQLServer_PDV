from dao.ProdutoDAO import *

dao = ProdutoDAO()

class ProdutoService:
    def insert(self, produto):
        dao.save(produto)

    def find_by_id(self, id):
        if self.__produto_eh_valido(id):
            return dao.find_by_id(id)

    def find_all(self):
        return dao.find_all()

    def update(self,id, produto):
        if self.__produto_eh_valido(id):
            dao.update(id, produto)

    def delete(self,id):
        if self.__produto_eh_valido(id):
            dao.delete(id)

    def __produto_eh_valido(self, id):
        produto = dao.find_by_id(id)
        if(produto != None):
            return True
        return False
