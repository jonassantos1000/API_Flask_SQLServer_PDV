from dao.connectionFactory.connection import *
import logging
from model.ItensPedido import *
from model.Produto import *
from exception.ExceptionHandler import *

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


class ItensPedidoDAO:
    def __init__(self):
        self._connection = connection()

    def find_itens_pedido_by_id(self, pedidoId):
        logging.info('METODO findItensPedidoById INICIADO')
        cursor = self._connection.cursor()
        try:
            cursor.execute('''
                                    SELECT 
                                    tip.id, tip.produto_id, tip.preco_unitario,tip.quantidade, tip.total,
                                    tp.descricao, tp.preco
                                    FROM estudos.tb_itens_pedido tip
                                    INNER JOIN estudos.tb_produto tp ON (tip.produto_id = tp.id)
                                    INNER JOIN estudos.pedido_venda pv ON (tip.pedido_venda_id = pv.id)
                                    where tip.pedido_venda_id = ?''', pedidoId)
            row = cursor.fetchone()
            listItens = []
            while row:
                produto = Produto(row.produto_id, row.descricao, float(row.preco)).dict()
                item = ItensPedido(row.id, produto, row.quantidade, float(row.preco_unitario), float(row.total)).dict()
                listItens.append(item)
                row = cursor.fetchone()

            return listItens
        except Exception as error:
            logging.error(
                f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findItensPedidoById de ItensPedidoDAO:\n {error.args}")
            raise Exception('OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findItensPedidoById de ItensPedidoDAO')
        finally:
            cursor.close()

    def save(self, listItem, idPedido, cursor):
        try:
            logging.info('METODO SAVE DE ItensPedidoDAO INICIADO')
            for item in listItem:
                cursor.execute('''
                    INSERT INTO estudos.tb_itens_pedido (produto_id,pedido_venda_id, preco_unitario, quantidade, total) 
                    values (?, ?, ?,?, ?)''', item.produto.id, idPedido, item.preco_unitario, item.quantidade, item.total)
        except Exception as error:
            logging.error(
                f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO save de ItensPedidoDAO:\n {error.args}")
            cursor.rollback()
            logging.error(f"FOI REALIZADO O ROLLBACK DO METODO save de ItensPedidoDAO")
            raise BadRequest('Parametros invalidos',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
        finally:
            logging.info('METODO SAVE DE ItensPedidoDAO FINALIZADO')

    def delete(self, idPedido, cursor):
        try:
            logging.info("METODO DELETE DE itensPedidoDAO INICIADO")
            cursor.execute('''DELETE FROM estudos.tb_itens_pedido where pedido_venda_id = ?''', idPedido)
        except:
            logging.error("OCORREU UM ERRO DURANTE A EXECUÇÃO DO METODO DELETE DE itensPedidoDAO")
            cursor.rollback()
            logging.error("EFETUADO ROLLBACK DO METODO DELETE DE itensPedidoDAO")
            raise BadRequest('Parametros invalidos',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
        finally:
            logging.info("METODO DELETE DE itensPedidoDao FINALIZADO")
