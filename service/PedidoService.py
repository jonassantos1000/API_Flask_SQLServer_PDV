from dao.PedidoDAO import *

dao = PedidoDAO()


class PedidoService:
    def insert(self, pedido):
        if len(pedido.itensPedido) == 0:
            raise IllegalArgument('Pedido Invalido', 'O pedido deve conter pelo menos 1 item')
        dao.save(pedido)

    def findById(self, id):
        if self.__pedidoEhValido(id):
            return dao.findById(id)

    def findAll(self):
        return dao.findAll()

    def update(self,id, pedido):
        if self.__pedidoEhValido(id):
            dao.update(id, pedido)

    def delete(self, id):
        if self.__pedidoEhValido(id):
            dao.delete(id)

    def __pedidoEhValido(self, id):
        pedido = dao.findById(id)
        if (pedido != None):
            return True
        return False
