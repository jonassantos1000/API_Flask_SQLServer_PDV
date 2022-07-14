from dao.connectionFactory.connection import connection
from model.Cliente import Cliente
from exception.exceptionHandler import *


class ClienteDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, cliente):
        try:
            self.gerarCursor()
            self._cursor.execute("""
            INSERT INTO estudos.tb_cliente (nome, endereco, telefone)
            VALUES (?,?,?)""", cliente.nome, cliente.endereco, cliente.telefone)
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def findAll(self):
        try:
            self.gerarCursor()
            self._cursor.execute(f'select * from estudos.tb_cliente')
            row = self._cursor.fetchone()
            listCliente = []
            while row:
                listCliente.append(Cliente(row.id, row.nome, row.endereco, row.telefone).dict())
                row = self._cursor.fetchone()
            return listCliente
        finally:
            self.finalizarConexao()

    def findById(self, id):
        try:
            self.gerarCursor()
            self._cursor.execute(f'select * from estudos.tb_cliente where id = {id}')
            row = self._cursor.fetchone()
            if row:
                cliente = Cliente(row.id, row.nome, row.endereco, row.telefone).dict()
                return cliente
            raise IllegalArgument('Id Invalido', 'Não foi possivel identificar um recurso cliente válido com o id ' + id)
        finally:
            self.finalizarConexao()

    def update(self, id, cliente):
        try:
            self.gerarCursor()
            self._cursor.execute('update estudos.tb_cliente set nome= ?, endereco= ?, telefone= ?  where id=?',
                                 cliente.nome, cliente.endereco, cliente.telefone, id)
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def delete(self, id):
        try:
            self.gerarCursor()
            self._cursor.execute(f'delete from estudos.tb_cliente where id = {id}')
            self._cursor.commit()
        finally:
            self.finalizarConexao()

    def gerarCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizarConexao(self):
        self._connection.close()
