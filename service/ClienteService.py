from dao.ClienteDAO import *

dao = ClienteDAO()


class ClienteService:
    def insert(self, cliente):
        dao.save(cliente)

    def update(self, id, cliente):
        if self.__clientEhValido(id):
            dao.update(id, cliente)
            return

    def findById(self, id):
        if self.__clientEhValido(id):
            return dao.findById(id)

    def findAll(self):
        return dao.findAll()

    def delete(self, id):
        if self.__clientEhValido(id):
            dao.delete(id)
            return

    def __clientEhValido(self, id):
        cliente = dao.findById(id)
        if (cliente != None):
            return True
        return False
