from dao.ItensPedidoDAO import *

dao = ItensPedidoDAO()

class ItensPedidoService:
    def findByIdPedido(self, id):
        return dao.findItensPedidoById(id)

    def insert(self, listItensPedido, idPedido):
        dao.save(listItensPedido, idPedido)

    def delete (self, idPedido):
        dao.delete(idPedido)