import pytest
import json
import requests

from model.ItensPedido import ItensPedido
from model.Pagamento import *
from model.Pedido import Pedido
from server import server
from model.Cliente import *
from model.Produto import *

app = server.app

url = "http://127.0.0.1:5000/pedido"

headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
    'Content-Type':'application/json'
}

@pytest.fixture
def geraPedido():
    valorTotal = 150.0
    dataVenda = "2022-07-14"
    cliente = Cliente(1,"Bruno","Rua dos pinheiros","(11) 98347-3443").dict()
    produto = Produto(1,"Bone nike preto", 150.0).dict()
    quantidade = 1
    precoUnitario= 150.0
    total= 150.0
    listItens = []
    item = ItensPedido(None, produto, quantidade, precoUnitario, total).dict()
    listItens.append(item)
    return Pedido(None, cliente, valorTotal, dataVenda, {}, listItens).dict()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_deveria_retornar_a_lista_completa_de_pedidos(client):
    response = requests.get(url)
    pedido = response.json()[0]
    dataVenda = pedido['dataVenda']

    assert 200 == response.status_code

def test_deveria_encontrar_pedido_pelo_id(client):
    response = requests.get(f'{url}/1')
    pedido = response.json()
    dataVenda = pedido['dataVenda']

    assert 200 == response.status_code


def test_nao_deveria_encontrar_pedido_com_id_inexistente(client):
    response = requests.get(f'{url}/0')
    assert 404 == response.status_code


def test_deveria_apagar_o_pedido_por_id(client,geraPedido):
    test_deveria_fazer_post_de_pedido(client, geraPedido)
    response = requests.get(f'{url}')
    tam = len(response.json())
    idPedido = response.json()[tam-1]['id']
    print(idPedido)
    response = requests.delete(f'{url}/{idPedido}')
    assert 204 == response.status_code

def test_deveria_retornar_erro_badrequest_ao_tentar_apagar_pedido_com_pagamento(client):
    response = requests.delete(f'{url}/1')
    assert 400 == response.status_code

def test_deveria_retornar_erro_badrequest_ao_tentar_apagar_pedido_com_id_inexistente(client):
    response = requests.delete(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_fazer_post_de_pedido(client, geraPedido):
    p = geraPedido
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 201 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_sem_cliente(client, geraPedido):
    p = geraPedido
    del p['cliente']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_dataVenda_pedido_vazio(client,geraPedido):
    p = geraPedido
    del p['dataVenda']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_sem_itensPedido(client,geraPedido):
    p = geraPedido
    del p['itensPedido']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_itensPedido_vazio(client,geraPedido):
    p = geraPedido
    del p['itensPedido'][0]
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_itensPedido_sem_Produto(client,geraPedido):
    p = geraPedido

    del p['itensPedido'][0]
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_itensPedido_sem_quantidade(client,geraPedido):
    p = geraPedido

    del p['itensPedido'][0]['quantidade']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_itensPedido_sem_precoUnitario(client,geraPedido):
    p = geraPedido

    del p['itensPedido'][0]['precoUnitario']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_pedido_com_itensPedido_sem_total(client,geraPedido):
    p = geraPedido

    del p['itensPedido'][0]['total']
    resposta = requests.post(url, headers=headers, data= json.dumps(p))
    assert 400 == resposta.status_code