import mysql.connector
import os
import subprocess
from mysql.connector import Error
from pymysql.constants.ER import DUP_ENTRY

'''Primeira versão do script das funções base de dados'''


# Connect to server
def create_server_connection():
    host = ""
    username = ""
    passwordd = ""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=passwordd
        )
    except Error as err:
        print(f"\nError: '{err}'")

    return connection


# Connector to MySQL Server and desired DataBase
def create_db_connection(db_name):
    host = ""
    username = ""
    passwordd = ""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=passwordd,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


# Create DataBase
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


# Query executer
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("\nQuery successful")
        return "Registada com sucesso na Base de dados!"
    except Error as err:
        if err.args[0] == DUP_ENTRY:
            return "Entrada já se encontra registada na base de dados!"
            # print('\r Entrada já se encontra registada na base de dados!', end="")
        else:
            print(f"\nError: '{err}'")


# Read information
def read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# Adding multiple data
def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def clone_db(database, new_database):
    try:
        if os.path.exists(fr'C:clone_{database}_db.bat'):
            subprocess.call([fr"C:clone_{database}_db.bat"])
            os.remove(fr"C:clone_{database}_db.bat")
        else:
            my_bat = open(fr'C:clone_{database}_db.bat', 'w+')
            my_bat.write(
                fr'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" --login-path=local {database}'
                fr' | "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" --login-path=local -p {new_database}')
            my_bat.close()
            subprocess.call([f"C:clone_{database}_db.bat"])
            os.remove(fr"C:clone_{database}_db.bat")
    except Exception as e:
        print("Erro ao clonar a base de dados: ")
        print(e)


def verify_database(server, database):
    try:
        query_verify_db = f"SHOW DATABASES LIKE '{database}'"
        result = read_query(server, query_verify_db)
        if len(result) == 0:
            return False
        else:
            return True
    except Exception as e:
        print("Erro ao verificar a base de dados: \n", e)


def get_credentials(db_connection):
    try:
        query_credentials = "SELECT * FROM fatura_credential"
        credentials = read_query(db_connection, query_credentials)
        return credentials
    except Exception as e:
        print("\nErro ao aceder as credenciais na base de dados: ")
        raise e
