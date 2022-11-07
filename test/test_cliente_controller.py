from time import time

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

@pytest.fixture()
def client():
    cliente = Cliente(2,"luan","Rua dos pinheiros","(11) 98347-3443", "testecontroller@gmail.com").dict()
    return cliente

def test_deveria_retornar_a_lista_completa_de_cliente():
    response = requests.get(url)
    assert 200 == response.status_code

def test_deveria_encontrar_cliente_pelo_id():
    response = requests.get(f'{url}/1')
    assert 200 == response.status_code
    assert 1 == response.json()['id']
    return response

def test_nao_deveria_encontrar_cliente_com_id_inexistente():
    response = requests.get(f'{url}/0')
    assert 404 == response.status_code

def test_deveria_fazer_post_de_cliente(client):
    cliente = client
    resposta = requests.post(url, headers=headers, data=json.dumps(cliente))
    clienteInserido = requests.get(url).json()
    assert clienteInserido[len(clienteInserido)-1]['nome'] == cliente.get('nome')
    assert 201 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_cliente_com_nome_vazio(client):
    cliente = client
    cliente.update({'nome':''})
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code

def test_deveria_retornar_badrequest_post_de_cliente_com_endereco_vazio(client):
    cliente = client
    cliente.update({'endereco':''})
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code


def test_deveria_retornar_badrequest_post_de_cliente_com_telefone_vazio(client):
    cliente = client
    cliente.update({'telefone':''})
    resposta = requests.post(url, headers=headers, data= json.dumps(cliente))
    print(resposta.text)
    assert 400 == resposta.status_code

def test_deveria_alterar_cliente(client):
    cliente = client
    cliente.update({'nome': 'alterado', 'endereco':'endereco alterado {}'.format(time()), 'telefone':'(20) 11111-1111', 'email':'alterado@gmail.com'})
    response = requests.put(f'{url}/1', headers=headers, data= json.dumps(cliente))
    assert 200 == response.status_code
    clienteAlterado = requests.get(f'{url}/1')
    assert cliente.get('nome') == clienteAlterado.json()['nome']
    assert cliente.get('endereco') == clienteAlterado.json()['endereco']
    assert cliente.get('telefone') == clienteAlterado.json()['telefone']
    assert cliente.get('email') == clienteAlterado.json()['email']

def test_deveria_apagar_um_cliente(client):
    resposta = requests.post(url, headers=headers, data= json.dumps(client))
    cliente = requests.get(url).json()
    idCliente = cliente[len(cliente)-1]['id']
    response = requests.delete(f'{url}/{idCliente}')
    assert 204 == response.status_code

def test_deveria_retornar_erro_ao_tentar_apagar_cliente_com_id_inexistente(client):
    response = requests.delete(f'{url}/0')
    assert 404 == response.status_code