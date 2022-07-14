import configparser
import pyodbc

cfg = configparser.ConfigParser()
cfg.read('datasource.ini')

def connection():
    server = cfg.get('datasource', 'server')
    database = cfg.get('datasource', 'database')
    username = cfg.get('datasource', 'username')
    password = cfg.get('datasource', 'password')
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn