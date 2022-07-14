from dao.PedidoDAO import *
from model.Pedido import *
from model.Cliente import *

dao = PedidoDAO()


class PedidoService:
    def insert(self, jsonPedido):
        valorTotal = jsonPedido['valorTotal']
        dataVenda = jsonPedido['dataVenda']
        cliente = Cliente(**jsonPedido['cliente'])
        pedido = Pedido(None, cliente, valorTotal, dataVenda)
        dao.save(pedido)

    def findById(self, id):
        if self.__pedidoEhValido(id):
            return dao.findById(id)

    def __pedidoEhValido(self, id):
        pedido = dao.findById(id)
        if (pedido != None):
            return True
        return False
