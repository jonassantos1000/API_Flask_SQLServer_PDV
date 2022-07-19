from dao.connectionFactory.connection import connection
from model.Cliente import Cliente
from exception.exceptionHandler import *
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


class ClienteDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, cliente):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO SAVE DE ClienteDAO')
            self._cursor.execute("""INSERT INTO estudos.tb_cliente (nome, endereco, telefone) VALUES (?,?,?)""", cliente.nome, cliente.endereco, cliente.telefone)
            self._cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO SAVE DE ClienteDAO:\n {error.args}')
            self._cursor.rollback()
            logging.error(f'REALIZADO ROLLBACK NO METODO save DE ClienteDAO')
        finally:
            logging.info('METODO SAVE DE ClienteDAO FINALIZADO')
            self.finalizarConexao()

    def findAll(self):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findAll DE ClienteDAO')
            self._cursor.execute(f'select * from estudos.tb_cliente SET NOCOUNT ON')
            row = self._cursor.fetchone()
            listCliente = []
            while row:
                listCliente.append(Cliente(row.id, row.nome, row.endereco, row.telefone).dict())
                row = self._cursor.fetchone()
            return listCliente
        except Exception as error:
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findALL de ClienteDAO:\n {error.args}")
        finally:
            logging.info('METODO findAll DE ClienteDAO FINALIZADO')
            self.finalizarConexao()

    def findById(self, id):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findById DE ClienteDAO')
            self._cursor.execute(f'select * from estudos.tb_cliente where id = {id}')
            row = self._cursor.fetchone()
            if row:
                cliente = Cliente(row.id, row.nome, row.endereco, row.telefone).dict()
                return cliente
            raise IllegalArgument('Id Invalido',
                                  'Não foi possivel identificar um recurso cliente válido com o id ' + id)
        finally:
            logging.info('METODO findById DE ClienteDAO FINALIZADO')
            self.finalizarConexao()

    def update(self, id, cliente):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO update DE ClienteDAO')
            self._cursor.execute('update estudos.tb_cliente set nome= ?, endereco= ?, telefone= ?  where id=?',
                                 cliente.nome, cliente.endereco, cliente.telefone, id)
            self._cursor.commit()
        except Exception as error:
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO update de ClienteDAO:\n {error.args}")
            self._cursor.rollback()
            logging.error(f"FOI REALIZADO O ROLLBACK DO METODO update de ClienteDAO")
        finally:
            logging.info('METODO update DE ClienteDAO FINALIZADO')
            self.finalizarConexao()

    def delete(self, id):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO delete DE ClienteDAO')
            self._cursor.execute(f'delete from estudos.tb_cliente where id = {id}')
            self._cursor.commit()
        except Exception as error:
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete de ClienteDAO:\n {error.args}")
            self._cursor.rollback()
            logging.error(f"FOI REALIZADO O ROLLBACK DO METODO delete de ClienteDAO")
        finally:
            logging.info('METODO delete DE ClienteDAO FINALIZADO')
            self.finalizarConexao()

    def gerarCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        self._connection.close()
