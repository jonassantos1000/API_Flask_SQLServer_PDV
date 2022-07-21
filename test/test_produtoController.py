import pytest
import json
import requests
from model.Produto import *
from server import server

app = server.app

url = "http://127.0.0.1:5000/produto"

headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
    'Content-Type':'application/json'
}


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_deveria_retornar_a_lista_completa_de_produto(client):
    response = requests.get(url)
    assert 200 == response.status_code

def test_deveria_encontrar_produto_pelo_id(client):
    response = requests.get(f'{url}/1')
    assert 200 == response.status_code

def test_nao_deveria_encontrar_produto_com_id_inexistente(client):
    response = requests.get(f'{url}/0')
    assert 404 == response.status_code


def test_deveria_fazer_post_de_Produto(client):
    produto = {"descricao": "Camiseta Puma", "preco": 200.0}
    resposta = requests.post(url, headers=headers, data= json.dumps(produto))
    assert 201 == resposta.status_code


def test_deveria_retornar_badrequest_post_de_produto_com_descricao_em_branco(client):
    produto = {"descricao": "", "preco": 200.0}
    resposta = requests.post(url, headers=headers, data= json.dumps(produto))
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_produto_com_preco_em_branco(client):
    produto = {"descricao": "Camiseta Puma", "preco": ""}
    resposta = requests.post(url, headers=headers, data= json.dumps(produto))
    assert 400 == resposta.status_code

def test_deveria_apagar_um_produto(client):
    response = requests.get(f'{url}')
    idProduto = response.json()[1]['id']
    response = requests.delete(f'{url}/{idProduto}')
    assert 204 == response.status_code

def test_deveria_retornar_erro_ao_tentar_apagar_cliente_com_id_inexistente(client):
    response = requests.delete(f'{url}/0')
    assert 404 == response.status_code