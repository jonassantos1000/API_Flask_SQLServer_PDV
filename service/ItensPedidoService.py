from dao.ItensPedidoDAO import *
from exception.ExceptionHandler import *

dao = ItensPedidoDAO()

class ItensPedidoService:
    def find_by_id_pedido(self, id):
        return dao.find_itens_pedido_by_id(id)

    def insert(self, listItensPedido, idPedido, connection):
        if self.__lista_de_itens_eh_valida(listItensPedido):
            dao.save(listItensPedido, idPedido, connection)

    def update(self, listItensPedido, idPedido, connection):
        if self.__lista_de_itens_eh_valida(listItensPedido):
            self.delete(idPedido,connection)
            self.insert(listItensPedido, idPedido, connection)

    def delete (self, idPedido, connection):
        dao.delete(idPedido, connection)

    def __lista_de_itens_eh_valida(self, listItensPedido):
        if len(listItensPedido) == 0:
            raise EmptyProductList('Pedido Invalido', 'O pedido deve conter pelo menos 1 item')

        return True