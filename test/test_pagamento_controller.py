import pytest
import json
import requests
from model.Pagamento import *
from model.Pedido import Pedido
from model.ItensPedido import *
from model.Cliente import *
from server import server

app = server.app

url = "http://127.0.0.1:5000/pagamento"

headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
    'Content-Type':'application/json'
}

@pytest.fixture
def geraPagamento():
    valorTotal = 150.0
    dataVenda = "2022-07-14"
    cliente = Cliente(2,"Bruno","Rua dos pinheiros","(11) 98347-3443", "teste@gmail.com").dict()
    produto = Produto(3,"Bone nike preto", 150.0).dict()
    quantidade = 1
    precoUnitario= 150.0
    total= 150.0
    listItens = []
    item = ItensPedido(None, produto, quantidade, precoUnitario, total).dict()
    listItens.append(item)
    pedido = Pedido(1, cliente, valorTotal, dataVenda, {}, listItens).dict()
    dataPagamento="2022-07-14"
    return Pagamento(None,pedido,dataPagamento).dict()

def test_deveria_retornar_a_lista_completa_de_pagamento():
    response = requests.get(url)
    assert 200 == response.status_code

def test_deveria_encontrar_pagamento_pelo_id():
    response = requests.get(f'{url}/1')
    assert 200 == response.status_code

def test_nao_deveria_encontrar_pagamento_com_id_inexistente():
    response = requests.get(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_excluir_o_pagamento_por_id():
    response = requests.delete(f'{url}/1')
    print(response.text)
    assert 204 == response.status_code

def test_deveria_retornar_erro_badrequest_ao_tentar_apagar_pagamento_com_id_inexistente():
    response = requests.delete(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_fazer_post_de_pagamento(geraPagamento):
    p = geraPagamento
    resposta = requests.post(url, headers=headers, data=json.dumps(p))
    print(resposta.text)
    assert 201 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_id_pedido_vazio(geraPagamento):
    p = geraPagamento
    del p['pedido']['id']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_sem_cliente(geraPagamento):
    p = geraPagamento
    del p['pedido']['cliente']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_dataVenda_pedido_vazio(geraPagamento):
    p = geraPagamento
    del p['pedido']['data_venda']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_sem_itensPedido(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_vazio(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido'][0]
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_Produto(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido'][0]['produto']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_quantidade(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido'][0]['quantidade']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_precoUnitario(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido'][0]['preco_unitario']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_total(geraPagamento):
    p = geraPagamento
    del p['pedido']['itens_pedido'][0]['total']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code