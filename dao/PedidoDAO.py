from dao.connectionFactory.connection import *
from model.Pedido import *
from model.Cliente import *
from model.PagamentoDTO import *
from service.ItensPedidoService import *
from exception.exceptionHandler import *
import logging

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

serviceItensPedido = ItensPedidoService()


class PedidoDAO:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def save(self, pedido):
        try:
            self.gerarCursor()
            logging.warning('INICIANDO METODO save DE PedidoDAO')
            self._cursor.execute(
                'insert into estudos.pedido_venda (valor_total, data_venda, cliente_id) OUTPUT Inserted.id values (?,?,?)',
                pedido.valorTotal, pedido.dataVenda, pedido.cliente.id)
            row = self._cursor.fetchone()
            pedidoId = row.id
            serviceItensPedido.insert(pedido.itensPedido, pedidoId, self._cursor)
            self._cursor.commit()
        except ListaDeProdutosVazia as error:
            logging.error(f'REALIZANDO ROLLBACK DO METODO save de PedidoDAO:\n {error.args}')
            self._cursor.rollback()
            raise ListaDeProdutosVazia('PEDIDO INVALIDO',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, O PEDIDO NÃO CONTEM ITENS VENDIDOS !')
        except Exception as error:
            logging.error(f'REALIZANDO ROLLBACK DO METODO save de PedidoDAO:\n {error.args}')
            self._cursor.rollback()
            raise BadRequest('PARAMETROS INVALIDOS',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
        finally:
            logging.warning('FINALIZANDO METODO save DE PedidoDAO')
            self.finalizaConexao()

    def findById(self, id):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findById de PedidoDAO')
            listItensPedido = []
            logging.info('INICIANDO SELECT PARA BUSCAR ITENS DO PEDIDO')

            self._cursor.execute(select + ' where pv.id = ?', id)
            row = self._cursor.fetchone()
            if row:
                return self.populaObjeto(row)
            logging.error(f"Pedido com id {id} não encontrado !")
            raise NotFound('Id Invalido', f"Pedido com id {id} não encontrado !")
        finally:
            logging.info('METODO findById DE PedidoDAO Finalizado')
            self.finalizaConexao()

    def findByIdCliente(self, id):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findByIdCliente de PedidoDAO')
            listItensPedido = []
            logging.info('INICIANDO SELECT PARA BUSCAR ITENS DO PEDIDO')

            self._cursor.execute(select + ' where pv.cliente_id = ?', id)
            listPedidos = []
            row = self._cursor.fetchone()
            while row:
                listPedidos.append(self.populaObjeto(row))
                row = self._cursor.fetchone()

            return listPedidos
        except Exception as error:
            logging.error("OCORREU UM ERRO DURANTE A EXECUÇÃO DO METODO FindByIdCliente")
            raise BadRequest("Falha na requisição", f"Error: {error.args}")
        finally:
            logging.info('METODO findById DE PedidoDAO Finalizado')
            self.finalizaConexao()

    def findAll(self):
        try:
            self.gerarCursor()
            logging.info('INICIANDO METODO findAll de PedidoDAO')
            self._cursor.execute(select)
            row = self._cursor.fetchone()
            listPedido = []
            while row:
                listPedido.append(self.populaObjeto(row))
                row = self._cursor.fetchone()
            return listPedido
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO findAll DE PedidoDAO:\n {error.args}')
            raise BadRequest('Parametros invalidos',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
        finally:
            logging.info('METODO findById DE PedidoDAO Finalizado')
            self.finalizaConexao()

    def delete(self, id):
        try:
            logging.info('METODO delete DE PedidoDAO INICIADO')
            self.gerarCursor()
            serviceItensPedido.delete(id, self._cursor)
            self._cursor.execute('DELETE FROM estudos.pedido_venda where id=?', id)
            self._cursor.commit()
        except pyodbc.IntegrityError as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete DE PedidoDAO:\n {error.args}')
            self._cursor.rollback()
            raise IntegrityError('VIOLACAO DE CONSTRAINT',
                                 'NÃO É POSSIVEL EXECUTAR ESTA AÇÃO, POIS O PEDIDO POSSUI PAGAMENTO VINCULADO')
            logging.error('REALIZADO ROLLBACK NO METODO delete DE PedidoDAO')
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO delete DE PedidoDAO:\n {error.args}')
            self._cursor.rollback()
            raise BadRequest('Parametros invalidos', 'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
            logging.error('REALIZADO ROLLBACK NO METODO delete DE PedidoDAO')
        finally:
            logging.info('METODO delete DE PedidoDAO FINALIZADO')
            self.finalizaConexao()

    def update(self, id, pedido):
        try:
            self.gerarCursor()
            logging.warning('METODO update DE PedidoDAO FINALIZADO')
            self._cursor.execute('update estudos.pedido_venda set valor_total=?, cliente_id=? where id=?',
                                 pedido.valorTotal,
                                 pedido.cliente.id, id)
            serviceItensPedido.update(pedido.itensPedido, id, self._cursor)
            self._cursor.commit()
        except Exception as error:
            logging.error(f'OCORREU UM ERRO DURANTE A EXECUCAO DO METODO update DE PedidoDAO:\n {error.args}')
            self._cursor.rollback()
            logging.error('REALIZADO ROLLBACK NO METODO update DE PedidoDAO')
            raise BadRequest('Parametros invalidos',
                             'NAO FOI POSSIVEL PROSSEGUIR COM A OPERACAO, VERIFIQUE AS INFORMACOES INSERIDAS !')
        finally:
            logging.warning('METODO update DE PedidoDAO FINALIZADO')
            self.finalizaConexao()

    def gerarCursor(self):
        self._connection = connection()
        self._cursor = self._connection.cursor()

    def finalizaConexao(self):
        self._connection.close()

    def populaObjeto(self, row):
        itens = serviceItensPedido.findByIdPedido(row.id)
        cliente = Cliente(row.cliente_id, row.nome, row.endereco, row.telefone).dict()
        pagamento = {"Status": "PENDENTE"}
        if row.pagamento_id != None:
            pagamento = PagamentoDTO(row.pagamento_id, str(row.data_pagamento), str("PAGO")).dict()

        return Pedido(row.id, cliente, float(row.valor_total), str(row.data_venda), pagamento, itens).dict()


select = '''select 
pv.id, pv.valor_total, pv.data_venda, pv.cliente_id, 
tc.nome, tc.endereco, tc.telefone,
tp.id as pagamento_id, tp.data_pagamento 
from estudos.pedido_venda pv 
inner join estudos.tb_cliente tc on (pv.cliente_id = tc.id)
left join estudos.tb_pagamento tp on (tp.pedido_venda_id=pv.id)
'''
