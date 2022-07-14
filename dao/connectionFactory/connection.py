import pyodbc

def connection():
    server = 'localhost'
    database = 'master'
    username = 'sa'
    password = 'Magna@123'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn