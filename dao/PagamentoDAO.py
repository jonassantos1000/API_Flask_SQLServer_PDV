import pyodbc
import logging
from dao.connectionFactory.connection import connection
from exception.exceptionHandler import *
from model.PagamentoDTO import *
from model.Cliente import *
from model.Pagamento import *
from model.Pedido import *
from service.ItensPedidoService import *

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

serviceItens = ItensPedidoService()


class PagamentoDAO:
    def __init__(self):
        self._connection = connection()

    def save(self, pagamento):
        cursor = self._connection.cursor()
        try:
            logging.info('METODO SAVE DE PagamentoDAO INICIADO')
            cursor.execute('''insert into estudos.tb_pagamento (pedido_venda_id, data_pagamento) values (?,?)''',
                                 pagamento.pedido.id, pagamento.dataPagamento)
            cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO SAVE DA ENTIDADE PAGAMENTODAO, ERRO:\n {error.args}')
            raise BadRequest('FALHA NA REQUISIÇÃO', 'PARAMETROS INVALIDOS, VERIFIQUE AS INFORMAÇÕES')
            cursor.rollback()
            cursor.cancel()
        finally:
            logging.info('METODO SAVE DE PagamentoDAO FINALIZADO')
            cursor.close()

    def findAll(self):
        cursor = self._connection.cursor()
        try:
            logging.info('METODO findAll de PagamentoDAO INICIADO')
            cursor.execute(select)
            row = cursor.fetchone()
            listPagamentos = []
            while row:
                listPagamentos.append(self.popularObjeto(row))
                row = cursor.fetchone()
            return listPagamentos
        except Exception as error:
            logging.error(f"ERRO AO PROCESSAR METODO findAll DE PagamentoDAO: {error.args}")
            cursor.cancel()
        finally:
            logging.info('METODO findAll de PagamentoDAO FINALIZADO')
            cursor.close()

    def findById(self, id):
        try:
            cursor = self._connection.cursor()
            cursor.execute(select + ' where tp.pedido_venda_id=?', id)
            row = cursor.fetchone()
            if row:
                return self.popularObjeto(row)
            logging.error(f'Não foi possivel encontrar um pagamento para o pedido com id {id}')
            raise NotFound('Id Invalido', f'Não foi possivel encontrar um pagamento para o pedido com id {id}')
        finally:
            logging.info(f'METODO findById FINALIZADO')
            cursor.close()

    def delete(self, id):
        try:
            cursor = self._connection.cursor()
            logging.info('METODO DELETE DE PagamentoDAO INICIADO')
            cursor.execute('DELETE FROM estudos.tb_pagamento where pedido_venda_id = ?', id)
            cursor.commit()
        except Exception as error:
            logging.error(f"ERRO AO PROCESSAR METODO delete DE PagamentoDAO: {error.args}")
            cursor.rollback()
            cursor.cancel()
            logging.error(f"FOI REALIZADO O ROLLBACK NO METODO delete DE PagamentoDAO")
        finally:
            logging.info('METODO DELETE DE PagamentoDAO FINALIZADO')
            cursor.close()

    def popularObjeto(self, row):
        cliente = Cliente(row.cliente_id, row.nome, row.endereco, row.telefone).dict()
        listItens = serviceItens.findByIdPedido(row.pedido_id)
        pedido = Pedido(row.pedido_id, cliente, float(row.valor_total), str(row.data_venda),
                        PagamentoDTO(row.pagamento_id, str(row.data_pagamento),"PAGO").dict(), listItens).dict()
        return Pagamento(row.pagamento_id, pedido, str(row.data_pagamento)).dict()


select = '''SELECT pv.id as pedido_id, pv.cliente_id, pv.valor_total, pv.data_venda, 
                                    tp.id as pagamento_id,tp.data_pagamento,
                                    tc.nome, tc.endereco, tc.telefone  
                                    from estudos.tb_pagamento tp
                                    inner join estudos.pedido_venda pv on (tp.pedido_venda_id=pv.id)
                                    INNER join estudos.tb_cliente tc on (pv.cliente_id=tc.id)'''
