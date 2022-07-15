from dao.connectionFactory.connection import connection
from model.Produto import *
from exception.exceptionHandler import *
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


class ProdutoDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, produto):
        try:
            self.geraCursor()
            logging.info('INICIANDO METODO SAVE DE ProdutoDAO')
            self._cursor.execute('''INSERT INTO estudos.tb_produto (descricao, preco) values (?,?)''',
                                 produto.descricao, float(produto.preco))
            self._cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO save DE ProdutoDAO:\n {error.args}')
            self._cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO save DE ProdutoDAO')
        finally:
            logging.info('METODO SAVE DE ProdutoDAO FINALIZADO')
            self.finalizarConexao()

    def findAll(self):
        try:
            self.geraCursor()
            logging.info('INICIANDO METODO FindAll DE ProdutoDAO')
            self._cursor.execute('select * from estudos.tb_produto')
            row = self._cursor.fetchone()
            listProduto = []
            while row:
                listProduto.append(Produto(row.id, row.descricao, float(row.preco)).dict())
                row = self._cursor.fetchone()
            return listProduto
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findAll DE ProdutoDAO:\n {error.args}')
        finally:
            logging.info('METODO FindAll DE ProdutoDAO FINALIZADO')
            self.finalizarConexao()

    def findById(self, id):
        try:
            self.geraCursor()
            logging.info('METODO FindById DE ProdutoDAO INICIADO')
            self._cursor.execute('''select * from estudos.tb_produto where id = ?''', id)
            row = self._cursor.fetchone()
            if row:
                produto = Produto(row.id, row.descricao, float(row.preco)).dict()
                return produto
            raise IllegalArgument('Id Invalido', 'Não foi possivel encontrar um recurso Produto válido com o id ' + id)
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findById DE ProdutoDAO:\n {error.args}')
        finally:
            logging.info('METODO findById DE ProdutoDAO FINALIZADO')
            self.finalizarConexao()

    def update(self, id, produto):
        try:
            self.geraCursor()
            logging.info('METODO update DE ProdutoDAO INICIADO')
            self._cursor.execute('UPDATE estudos.tb_produto SET descricao=?, preco=? WHERE ID= ?', produto.descricao,
                                 produto.preco, id)
            self._cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO update DE ProdutoDAO:\n {error.args}')
            self._cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO update DE ProdutoDAO')
        finally:
            logging.info('METODO update DE ProdutoDAO FINALIZADO')
            self.finalizarConexao()

    def delete(self, id):
        try:
            self.geraCursor()
            logging.info('METODO delete DE ProdutoDAO INICIADO')
            self._cursor.execute('DELETE FROM estudos.tb_produto where id= ?', id)
            self._cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete DE ProdutoDAO:\n {error.args}')
            self._cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO delete DE ProdutoDAO')
        finally:
            logging.info('METODO delete DE ProdutoDAO FINALIZADO')
            self.finalizarConexao()

    def geraCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        self._connection.close();
