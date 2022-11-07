from dao.PagamentoDAO import *

dao = PagamentoDAO()

class PagamentoService:
    def insert(self, pagamento):
        dao.save(pagamento)

    def find_all(self):
        return dao.find_all()

    def find_by_id(self, id):
        if self.__pagamento_eh_valido(id):
            return dao.find_by_id(id)

    def delete(self, id):
        if self.__pagamento_eh_valido(id):
            return dao.delete(id)

    def __pagamento_eh_valido(self, id):
        pagamento = dao.find_by_id(id)
        print(pagamento)
        if(pagamento != None):
            return True
        return False