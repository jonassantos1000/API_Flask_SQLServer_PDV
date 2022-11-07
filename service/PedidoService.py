import threading

from dao.PedidoDAO import *
from service.EmailService import *

dao = PedidoDAO()


class PedidoService:
    def insert(self, pedido):
        pedido = dao.save(pedido)
        self.__enviar_pedido_por_email(pedido)

    def find_by_id(self, id):
        if self.__pedido_eh_valido(id):
            return dao.find_by_id(id)

    def find_by_id_cliente(self, id):
        return dao.find_by_id_cliente(id)

    def find_all(self):
        return dao.find_all()

    def update(self,id, pedido):
        if self.__pedido_eh_valido(id):
            dao.update(id, pedido)

    def delete(self, id):
        if self.__pedido_eh_valido(id):
            dao.delete(id)

    def __pedido_eh_valido(self, id):
        pedido = dao.find_by_id(id)
        if (pedido != None):
            return True
        return False

    def __enviar_pedido_por_email(self, pedido):
        assunto = f'Pedido {pedido.id}'
        mensagem = f'Voce realizou a compra de {len(pedido.itens_pedido)} itens em nossa loja.\n Total: {pedido.valor_total}'
        threading.Thread(target=send, args=[pedido.cliente.email, assunto, mensagem]).start()
