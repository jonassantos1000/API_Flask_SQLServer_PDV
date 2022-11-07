from dao.connectionFactory.connection import connection
from model.Produto import *
from exception.ExceptionHandler import *
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


class ProdutoDAO:
    def __init__(self):
        try:
            self._connection = connection()
        except:
            raise BadRequest('Falha na requisição', 'Não foi possivel processar a requisição')

    def save(self, produto):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO SAVE DE ProdutoDAO')
            cursor.execute('''INSERT INTO estudos.tb_produto (descricao, preco) values (?,?)''',
                                 produto.descricao, float(produto.preco))
            cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO save DE ProdutoDAO:\n {error.args}')
            cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO save DE ProdutoDAO')
        finally:
            logging.info('METODO SAVE DE ProdutoDAO FINALIZADO')
            cursor.close()

    def find_all(self):
        try:
            cursor = self._connection.cursor()
            logging.info('INICIANDO METODO FindAll DE ProdutoDAO')
            cursor.execute('select * from estudos.tb_produto')
            row = cursor.fetchone()
            listProduto = []
            while row:
                listProduto.append(Produto(row.id, row.descricao, float(row.preco)).dict())
                row = cursor.fetchone()
            return listProduto
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findAll DE ProdutoDAO:\n {error.args}')
        finally:
            logging.info('METODO FindAll DE ProdutoDAO FINALIZADO')
            cursor.close()

    def find_by_id(self, id):
        try:
            cursor = self._connection.cursor()
            logging.info('METODO FindById DE ProdutoDAO INICIADO')
            cursor.execute('''select * from estudos.tb_produto where id = ?''', id)
            row = cursor.fetchone()
            if row:
                produto = Produto(row.id, row.descricao, float(row.preco)).dict()
                return produto
            raise NotFound('Id Invalido', 'Não foi possivel encontrar um recurso Produto válido com o id ' + id)
        finally:
            logging.info('METODO findById DE ProdutoDAO FINALIZADO')
            cursor.close()

    def update(self, id, produto):
        try:
            cursor = self._connection.cursor()
            logging.info('METODO update DE ProdutoDAO INICIADO')
            cursor.execute('UPDATE estudos.tb_produto SET descricao=?, preco=? WHERE ID= ?', produto.descricao,
                                 produto.preco, id)
            cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO update DE ProdutoDAO:\n {error.args}')
            cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO update DE ProdutoDAO')
        finally:
            logging.info('METODO update DE ProdutoDAO FINALIZADO')
            cursor.close()

    def delete(self, id):
        try:
            cursor = self._connection.cursor()
            logging.info('METODO delete DE ProdutoDAO INICIADO')
            cursor.execute('DELETE FROM estudos.tb_produto where id= ?', id)
            cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete DE ProdutoDAO:\n {error.args}')
            cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO delete DE ProdutoDAO')
        finally:
            logging.info('METODO delete DE ProdutoDAO FINALIZADO')
            cursor.close()
