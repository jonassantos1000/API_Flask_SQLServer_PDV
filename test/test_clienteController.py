import pytest
import json
import requests
from model.Cliente import *
from server import server

app = server.app

url = "http://127.0.0.1:5000/cliente"

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


def test_deveria_retornar_a_lista_completa_de_cliente(client):
    response = requests.get(url)
    clientes = response.json()[0]
    nome = clientes['nome']
    endereco = clientes['endereco']

    assert 200 == response.status_code
    assert 'Matheus Vieira' == nome
    assert 'Rua do amaral' == endereco

def test_deveria_encontrar_cliente_pelo_id(client):
    response = requests.get(f'{url}/2')
    nome = response.json()['nome']
    endereco = response.json()['endereco']

    assert 200 == response.status_code
    assert 'Matheus Vieira' == nome
    assert 'Rua do amaral' == endereco


def test_nao_deveria_encontrar_cliente_com_id_inexistente(client):
    response = requests.get(f'{url}/0')
    assert 400 == response.status_code


def test_deveria_fazer_post_de_cliente(client):
    cliente = {"nome": "teste unitario","endereco":"Rua dos pinheiros","telefone": "(11) 98632-7777"}
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 201 == resposta.status_code


def test_deveria_retornar_badrequest_post_de_cliente_com_nome_vazio(client):
    cliente = {"nome": "","endereco":"Rua dos pinheiros","telefone": "(11) 98632-7777"}
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_cliente_com_endereco_vazio(client):
    cliente = {"nome": "teste unitario","endereco":"","telefone": "(11) 98632-7777"}
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code


def test_deveria_retornar_badrequest_post_de_cliente_com_telefone_vazio(client):
    cliente = {"nome": "teste","endereco":"Rua dos pinheiros","telefone": ""}
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code

def test_deveria_apagar_um_cliente(client):
    response = requests.get(f'{url}')
    idCliente = response.json()[1]['id']
    response = requests.delete(f'{url}/{idCliente}')
    assert 204 == response.status_code

def test_deveria_retornar_erro_ao_tentar_apagar_cliente_com_id_inexistente(client):
    response = requests.delete(f'{url}/0')
    assert 400 == response.status_code