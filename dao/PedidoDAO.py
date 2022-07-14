from dao.connectionFactory.connection import *
from model.Pedido import *
from model.Cliente import *
from exception.exceptionHandler import *
import logging

logging.basicConfig(format = "%(asctime)s %(message)s", level=logging.DEBUG)


class PedidoDAO:
    def __init__(self):
        self._connection = None
        self._cursor= None

    def save(self, pedido):
        try:
            self.gerarCursor()
            logging.warning('INICIANDO METODO save DE PedidoDAO')
            self._cursor.execute('insert into estudos.pedido_venda (valor_total, data_venda, cliente_id) values (?,?,?)',
                                 pedido.valorTotal, pedido.dataVenda, pedido.cliente.id)
            self._cursor.commit()
        finally:
            logging.warning('FINALIZANDO METODO save DE PedidoDAO')
            self._cursor.close()

    def findById(self,id):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findById de PedidoDAO')
            self._cursor.execute('''
            select pv.id, pv.valor_total, pv.data_venda, pv.cliente_id, tc.nome, tc.endereco, tc.telefone  
            from estudos.pedido_venda pv 
            inner join estudos.tb_cliente tc on (pv.id = tc.id) 
            where pv.id = ?''', id)

            row = self._cursor.fetchone()
            if row:
                cliente = Cliente(row.cliente_id,row.nome,row.endereco,row.telefone).dict()
                pedido = Pedido(row.id,cliente, float(row.valor_total), str(row.data_venda))
                return pedido.dict()
            self.finalizaConexao()
            logging.error(f"Pedido com id {id} não encontrado !")
            raise IllegalArgument('Id Invalido', f"Pedido com id {id} não encontrado !")
        finally:
            logging.info('METODO findById DE PedidoDAO Finalizado')
            self._cursor.close()

    def findAll(self):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findAll de PedidoDAO')
            self._cursor.execute('''
            select pv.id, pv.valor_total, pv.data_venda, pv.cliente_id, tc.nome, tc.endereco, tc.telefone  
            from estudos.pedido_venda pv 
            inner join estudos.tb_cliente tc on (pv.id = tc.id)''')

            row = self._cursor.fetchone()
            listPedido=[]
            while row:
                cliente = Cliente(row.cliente_id,row.nome,row.endereco,row.telefone).dict()
                pedido = Pedido(row.id,cliente, float(row.valor_total), str(row.data_venda))
                listPedido.append(pedido.dict())
            self.finalizaConexao()
            return listPedido
        finally:
            logging.info('METODO findById DE PedidoDAO Finalizado')
            self._cursor.close()

    def 


    def gerarCursor(self):
        logging.info("CONEXAO COM BANCO DE DADOS INICIADO")
        self._connection=connection()
        self._cursor = self._connection.cursor()

    def finalizaConexao(self):
        logging.info("CONEXAO COM BANCO DE DADOS FINALIZADO")
        self._connection.close()