from dao.ClienteDAO import *

dao = ClienteDAO()


class ClienteService:
    def insert(self, cliente):
        return dao.save(cliente)

    def update(self, id, cliente):
        if self.__cliente_eh_valido(id):
            dao.update(id, cliente)
            return

    def find_by_id(self, id):
        if self.__cliente_eh_valido(id):
            return dao.find_by_id(id)

    def find_all(self):
        return dao.find_all()

    def delete(self, id):
        if self.__cliente_eh_valido(id):
            dao.delete(id)
            return

    def __cliente_eh_valido(self, id):
        cliente = dao.find_by_id(id)
        if (cliente != None):
            return True
        return False
