from dao.ItensPedidoDAO import *
from exception.exceptionHandler import *

dao = ItensPedidoDAO()

class ItensPedidoService:
    def findByIdPedido(self, id):
        return dao.findItensPedidoById(id)

    def insert(self, listItensPedido, idPedido):
        if self.__listaDeItensEhValida(listItensPedido):
            dao.save(listItensPedido, idPedido)

    def update(self, listItensPedido, idPedido):
        if self.__listaDeItensEhValida(listItensPedido):
            self.delete(idPedido)
            self.insert(listItensPedido, idPedido)

    def delete (self, idPedido):
        dao.delete(idPedido)

    def __listaDeItensEhValida(self, listItensPedido):
        if len(listItensPedido) == 0:
            raise IllegalArgument('Pedido Invalido', 'O pedido deve conter pelo menos 1 item')

        return True