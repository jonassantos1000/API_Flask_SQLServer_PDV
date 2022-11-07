#utilizando protocolo smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
import configparser


cfg = configparser.ConfigParser()
cfg.read('config/mail.ini')

host = cfg.get('mail','host')
port = cfg.getint('mail','port')
user = cfg.get('mail','email')
senha = cfg.get('mail','senha')

def send(destino, assunto, mensagem):
    conexao = conectar()
    msg = criar_mensagem(destino, assunto, mensagem)
    try:
        conexao.send_message(msg)
    except Exception as error:
        logging.error(f'Não foi possivel realizar o envio\nErro: {error.args}')

def conectar():
    try:
        conexao = smtplib.SMTP(host=host, port=port)
        conexao.starttls()
        conexao.login(user, senha)
        return conexao
    except smtplib.SMTPAuthenticationError as error:
        logging.error(f'Não foi possivel se autenticar ao e-mail\nErro: {error.args}')

def criar_mensagem(destino, assunto, mensagem):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = destino
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))
    return msg