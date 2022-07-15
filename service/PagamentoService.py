from dao.PagamentoDAO import *

dao = PagamentoDAO()

class PagamentoService:
    def insert(self, pagamento):
        dao.save(pagamento)

    def findAll(self):
        return dao.findAll()

    def findById(self, id):
        if self.__PagamentoEhValido(id):
            return dao.findById()

    def delete(self, id):
        if self.__PagamentoEhValido():
            return dao.delete(id)

    def __PagamentoEhValido(self, id):
        pagamento = dao.findById(id)
        if(pagamento != None):
            return True
        return False