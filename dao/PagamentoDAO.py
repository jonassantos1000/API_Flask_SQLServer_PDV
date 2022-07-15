import pyodbc
import logging
from dao.connectionFactory.connection import connection
from exception.exceptionHandler import *
from model.Cliente import *
from model.Pagamento import *
from model.Pedido import *

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

select = '''SELECT pv.id as pedido_id, pv.cliente_id, pv.valor_total, pv.data_venda, 
                                    tp.id as pagamento_id,tp.data_pagamento,
                                    tc.nome, tc.endereco, tc.telefone  
                                    from estudos.tb_pagamento tp
                                    inner join estudos.pedido_venda pv on (tp.pedido_venda_id=pv.id)
                                    INNER join estudos.tb_cliente tc on (pv.cliente_id=tc.id)'''


class PagamentoDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, pagamento):
        try:
            logging.info('METODO SAVE DE PagamentoDAO INICIADO')
            self.geraCursor()
            self._cursor.execute('''insert into estudos.tb_pagamento (pedido_venda_id, data_pagamento) values (?,?)''',
                                 pagamento.pedido.id, pagamento.dataPagamento)
            self._cursor.commit()
        except pyodbc.IntegrityError as error:
            logging.error(f"ERRO AO PROCESSAR METODO save DE PagamentoDAO: {error.args}")
            raise IntegrityError('Violação de constraint',
                                 'Operação não suportada, pois, este pedido já possui pagamento vinculado')
        finally:
            logging.info('METODO SAVE DE PagamentoDAO FINALIZADO')
            self.finalizarConexao()

    def findAll(self):
        try:
            self.geraCursor()
            logging.info('METODO findAll de PagamentoDAO INICIADO')
            self._cursor.execute(select)
            row = self._cursor.fetchone()
            listPagamentos = []
            while row:
                listPagamentos.append(self.popularObjeto(row))
                row = self._cursor.fetchone()
            return listPagamentos
        finally:
            logging.info('METODO findAll de PagamentoDAO FINALIZADO')
            self.finalizarConexao()

    def findById(self, id):
        try:
            self.geraCursor()
            self._cursor.execute(select + ' where id=?', id)
            row = self._cursor.fetchone()
            if row:
                return self.popularObjeto(row)
            logging.error(f'Não foi possivel encontrar um recurso pagamento com o id {id}')
            raise IllegalArgument('Id Invalido', f'Não foi possivel encontrar um recurso pagamento com o id {id}')
        finally:
            logging.info(f'METODO findById FINALIZADO')
            self.finalizarConexao()

    def delete(self, id):
        try:
            self.geraCursor()
            logging.info('METODO DELETE DE PagamentoDAO INICIADO')
            self._cursor.execute('DELETE FROM estudos.tb_pagamento where id = ?', id)
            self._cursor.commit()
        finally:
            logging.info('METODO DELETE DE PagamentoDAO FINALIZADO')
            self.finalizarConexao()

    def geraCursor(self):
        logging.info('CONEXAO COM BANCO DE DADOS INICIALIZADA')
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        logging.info('CONEXAO COM BANCO DE DADOS FINALIZADA')
        self._cursor.close()

    def popularObjeto(self, row):
        cliente = Cliente(row.cliente_id, row.nome, row.endereco, row.telefone).dict()
        pedido = Pedido(row.pedido_id, cliente, float(row.valor_total), str(row.data_venda)).dict()
        return Pagamento(row.pagamento_id, pedido, str(row.data_pagamento)).dict()