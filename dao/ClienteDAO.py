from model.Cliente import Cliente
from exception.ExceptionHandler import *
from dao.connectionFactory.connection import *
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


class ClienteDAO:

    def __init__(self):
        try:
            self._connection = connection()
        except:
            raise BadRequest('Falha na requisição', 'Não foi possivel processar a requisição')

    def save(self, cliente):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO SAVE DE ClienteDAO')
            cursor.execute("""INSERT INTO estudos.tb_cliente (nome, endereco, telefone, email) OUTPUT Inserted.id VALUES (?,?,?,?)""", cliente.nome, cliente.endereco, cliente.telefone, cliente.email)
            row = cursor.fetchone()
            id = row.id
            cursor.commit()
            logging.info(f'SAVE REALIZADO COM SUCESSO !')
            cliente.id=id
            return cliente.dict()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO SAVE DE ClienteDAO:\n {error.args}')
            cursor.rollback()
            logging.error(f'REALIZADO ROLLBACK NO METODO save DE ClienteDAO')
        finally:
            logging.info('METODO SAVE DE ClienteDAO FINALIZADO')
            cursor.close()

    def find_all(self):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO findAll DE ClienteDAO')
            cursor.execute(f'select * from estudos.tb_cliente SET NOCOUNT ON')
            rows = cursor.fetchall()
            listCliente = []
            for row in rows:
                listCliente.append(Cliente(row.id, row.nome, row.endereco, row.telefone, row.email).dict())
            return listCliente
        except Exception as error:
            cursor.cancel()
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findALL de ClienteDAO:\n {error.args}")
        finally:
            logging.info('METODO findAll DE ClienteDAO FINALIZADO')
            cursor.close()

    def find_by_id(self, id):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO findById DE ClienteDAO')
            cursor.execute(f'select * from estudos.tb_cliente where id = {id}')
            row = cursor.fetchone()
            if row:
                cliente = Cliente(row.id, row.nome, row.endereco, row.telefone, row.email).dict()
                return cliente
            raise NotFound('Id Invalido',
                                  'Não foi possivel identificar um recurso cliente válido com o id ' + str(id))
        finally:
            logging.info('METODO findById DE ClienteDAO FINALIZADO')
            cursor.close()

    def update(self, id, cliente):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO update DE ClienteDAO')
            cursor.execute('update estudos.tb_cliente set nome= ?, endereco= ?, telefone= ?,  email= ? where id=?',
                                 cliente.nome, cliente.endereco, cliente.telefone,cliente.email, id)
            cursor.commit()
        except Exception as error:
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO update de ClienteDAO:\n {error.args}")
            cursor.rollback()
            logging.error(f"FOI REALIZADO O ROLLBACK DO METODO update de ClienteDAO")
        finally:
            logging.info('METODO update DE ClienteDAO FINALIZADO')
            cursor.close()

    def delete(self, id):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO delete DE ClienteDAO')
            cursor.execute(f'delete from estudos.tb_cliente where id = {id}')
            cursor.commit()
        except Exception as error:
            logging.error(f"OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete de ClienteDAO:\n {error.args}")
            cursor.rollback()
            logging.error(f"FOI REALIZADO O ROLLBACK DO METODO delete de ClienteDAO")
        finally:
            logging.info('METODO delete DE ClienteDAO FINALIZADO')
            cursor.close()
