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
    cliente = Cliente(2,"Bruno","Rua dos pinheiros","(11) 98347-3443").dict()
    produto = Produto(3,"Bone nike preto", 150.0).dict()
    quantidade = 1
    precoUnitario= 150.0
    total= 150.0
    listItens = []
    item = ItensPedido(None, produto, quantidade, precoUnitario, total).dict()
    listItens.append(item)
    pedido = Pedido(2, cliente, valorTotal, dataVenda, {}, listItens).dict()
    dataPagamento="2022-07-14"
    return Pagamento(None,pedido,dataPagamento).dict()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_deveria_retornar_a_lista_completa_de_pagamento(client):
    response = requests.get(url)
    assert 200 == response.status_code

def test_deveria_encontrar_pagamento_pelo_id(client):
    response = requests.get(f'{url}/1')

    assert 200 == response.status_code

def test_nao_deveria_encontrar_pagamento_com_id_inexistente(client):
    response = requests.get(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_excluir_o_pagamento_por_id(client):
    response = requests.delete(f'{url}/2')
    print(response.text)
    assert 204 == response.status_code

def test_deveria_retornar_erro_badrequest_ao_tentar_apagar_pagamento_com_id_inexistente(client):
    response = requests.delete(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_fazer_post_de_pagamento(client, geraPagamento):
    p = geraPagamento
    resposta = requests.post(url, headers=headers, data=json.dumps(p))
    print(resposta.text)
    assert 201 == resposta.status_code


def test_deveria_retornar_badrequest_post_de_pagamento_com_id_pedido_vazio(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['id']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_sem_cliente(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['cliente']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_dataVenda_pedido_vazio(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['dataVenda']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_sem_itensPedido(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_vazio(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido'][0]
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_Produto(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido'][0]['produto']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_quantidade(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido'][0]['quantidade']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_precoUnitario(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido'][0]['precoUnitario']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pagamento_com_itensPedido_sem_total(client, geraPagamento):
    p = geraPagamento
    del p['pedido']['itensPedido'][0]['total']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code