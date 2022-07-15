from dao.connectionFactory.connection import *
import logging
from model.ItensPedido import *
from model.Produto import *

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

class ItensPedidoDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def findItensPedidoById(self, pedidoId):
        try:
            self.gerarCursor()
            logging.info('METODO findItensPedidoById INICIADO')
            self._cursor.execute('''
                                    SELECT 
                                    tip.id, tip.produto_id, tip.quantidade, tip.total,
                                    tp.descricao, tp.preco
                                    FROM estudos.tb_itens_pedido tip
                                    INNER JOIN estudos.tb_produto tp ON (tip.produto_id = tp.id)
                                    INNER JOIN estudos.pedido_venda pv ON (tip.pedido_venda_id = pv.id)
                                    where tip.pedido_venda_id = ?''', pedidoId)
            row = self._cursor.fetchone()
            listItens = []
            while row:
                produto = Produto(row.produto_id, row.descricao, float(row.preco)).dict()
                item = ItensPedido(row.id, produto, row.quantidade, float(row.total)).dict()
                listItens.append(item)
                row = self._cursor.fetchone()
        finally:
            self.finalizarConexao()

        return listItens

    def save(self, listItem, idPedido):
        try:
            self.gerarCursor()
            for item in listItem:
                self._cursor.execute('''
                    INSERT INTO estudos.tb_itens_pedido (produto_id,pedido_venda_id, quantidade, total) 
                    values (?, ?, ?, ?)''', item.produto.id, idPedido, item.quantidade, item.total)
            self._cursor.commit()
        finally:
            self.finalizarConexao()



    def gerarCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        self._connection.close()