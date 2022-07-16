from dao.ItensPedidoDAO import *
from exception.exceptionHandler import *

dao = ItensPedidoDAO()

class ItensPedidoService:
    def findByIdPedido(self, id):
        return dao.findItensPedidoById(id)

    def insert(self, listItensPedido, idPedido, connection):
        if self.__listaDeItensEhValida(listItensPedido):
            dao.save(listItensPedido, idPedido, connection)

    def update(self, listItensPedido, idPedido, connection):
        if self.__listaDeItensEhValida(listItensPedido):
            self.delete(idPedido,connection)
            self.insert(listItensPedido, idPedido, connection)

    def delete (self, idPedido, connection):
        dao.delete(idPedido, connection)

    def __listaDeItensEhValida(self, listItensPedido):
        if len(listItensPedido) == 0:
            raise IllegalArgument('Pedido Invalido', 'O pedido deve conter pelo menos 1 item')

        return True