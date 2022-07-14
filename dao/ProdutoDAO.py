from dao.connectionFactory.connection import connection
from model.Produto import *
from exception.exceptionHandler import *


class ProdutoDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, produto):
        try:
            self.geraCursor()
            self._cursor.execute('''INSERT INTO estudos.tb_produto (descricao, preco) values (?,?)''',
                                 produto.descricao, float(produto.preco))
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def findAll(self):
        try:
            self.geraCursor()
            self._cursor.execute('select * from estudos.tb_produto')
            row= self._cursor.fetchone()
            listProduto=[]
            while row:
                listProduto.append(Produto(row.id, row.descricao,float(row.preco)).dict())
                row= self._cursor.fetchone()
            return listProduto
        finally:
            self.finalizarConexao()

    def findById(self, id):
        try:
            self.geraCursor()
            self._cursor.execute('''select * from estudos.tb_produto where id = ?''', id)
            row = self._cursor.fetchone()
            if row:
                produto = Produto(row.id, row.descricao,float(row.preco)).dict()
                return produto
            raise IllegalArgument('Id Invalido', 'Não foi possivel encontrar um recurso Produto válido com o id '+id)
        finally:
            self.finalizarConexao()

    def update(self, id, produto):
        try:
            self.geraCursor()
            self._cursor.execute('UPDATE estudos.tb_produto SET descricao=?, preco=? WHERE ID= ?', produto.descricao, produto.preco, id)
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def delete(self, id):
        try:
            self.geraCursor()
            self._cursor.execute('DELETE FROM estudos.tb_produto where id= ?', id)
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def geraCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        self._connection.close();
