import configparser
import logging
import pyodbc

cfg = configparser.ConfigParser()
cfg.read('config/datasource.ini')
server = cfg.get('datasource', 'server')
database = cfg.get('datasource', 'database')
username = cfg.get('datasource', 'username')
password = cfg.get('datasource', 'password')

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def connection():
    try:
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER='+server+
                              ';DATABASE='+database+
                              ';UID='+username+
                              ';PWD='+ password+
                              ';MARS_Connection=yes')
        return cnxn
    except Exception as error:
        logging.error("Ocorre um erro ao criar conexao no banco de dados")
