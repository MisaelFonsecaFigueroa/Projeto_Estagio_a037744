import sys
import mysql.connector
import os
import subprocess
from mysql.connector import Error
from pymysql.constants.ER import DUP_ENTRY

'''Última versão do script que contêm as funções da base de dados que os robôs utilizam'''

# host Data
Host = ""
Username = ""
Password = ""


# Connect to server
def create_server_connection():
    host = Host
    username = Username
    password = Password
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password
        )
    except Error as err:
        print(f"\nError: '{err}'")
        sys.exit(1)

    return connection


db = create_server_connection()


# Connector to MySQL Server and desired DataBase
def create_db_connection(db_name):
    host = Host
    username = Username
    password = Password
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=db_name
        )
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
        return "Registo com sucesso na Base de dados!"
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


def get_fornecedores(db_connection):
    try:
        query_credentials = "SELECT * FROM nif_fornecedores"
        credentials = read_query(db_connection, query_credentials)
        return credentials
    except Exception as e:
        print("\nErro ao aceder os fornecedores na base de dados: ")
        raise e


query_tabela = """
CREATE TABLE fatura (
  num_fatura varchar(50) not null,
  setor VARCHAR(50) NULL,
  nif_consumidor VARCHAR(20) NOT NULL,
  nome_consumidor VARCHAR(50) NULL,
  nif_comerciante VARCHAR(255) NOT NULL,
  nome_comerciante VARCHAR(255) NULL, 
  tipo_fatura VARCHAR(255) NULL,
  registada_por VARCHAR(255) NULL,
  situacao VARCHAR(255) NULL,
  data_emissao VARCHAR(255) NULL,
  cod_controlo VARCHAR(255) NULL,
  total VARCHAR(255) NULL,
  iva_total VARCHAR(255) NULL,
  base_tributavel_total VARCHAR(255) NULL,
  taxa_1 VARCHAR(255) NULL,
  iva_1 VARCHAR(255) NULL,
  taxa_2 VARCHAR(255) NULL,
  iva_2 VARCHAR(255) NULL,
  taxa_3 VARCHAR(255) NULL,
  iva_3 VARCHAR(255) NULL,
  taxa_4 VARCHAR(255) NULL,
  iva_4 VARCHAR(255) NULL,
  lancado boolean default false,
  artigoL1 text NULL,
  artigoL2 text NULL,
  artigoL3 text NULL,
  artigoL4 text NULL,
  baseL5 text NULL,
  valorIVA_L5 text NULL,
  artigoL5 text NULL,
  pagamento text NULL,
  pendente boolean default false,
  tipo_documento text NULL,
  n_lancamento text NULL,
  classifcado boolean default false,
  codigo_IVA_L1 text NULL,
  codigo_IVA_L2 text NULL,
  codigo_IVA_L3 text NULL,
  codigo_IVA_L4 text NULL,
  codigo_IVA_L5 text NULL,
  concilidado boolean default false,
  id_pagamento text NULL,
  id_linha text NULL,
  valor_pago text NULL,
  miv_manual boolean default false,
  rf boolean default false,
  taxa_rf text NULL,
  valor_rf text NULL,
  data_importacao text NULL,
  taxa_IVA_L1 text NULL,
  taxa_IVA_L2 text NULL,
  taxa_IVA_L3 text NULL,
  taxa_IVA_L4 text NULL,
  taxa_IVA_L5 text NULL,
  total_L1 text NULL,
  total_L2 text NULL,
  total_L3 text NULL,
  total_L4 text NULL,
  total_L5 text NULL,
  n_linha_L1 text NULL,
  n_linha_L2 text NULL,
  n_linha_L3 text NULL,
  n_linha_L4 text NULL,
  n_linha_L5 text NULL,
  seccao text NULL,
  tpDoc text NULL,
  codExercicio text NULL,
  codPag text NULL,
  moeda text NULL,
  cambio text NULL,
  login text NULL,
  mercado text NULL,
  estadoDoc text NULL,
  dataEstado text NULL,
  totalMercadoriaSIVA text NULL,
  meioExpedicao text NULL,
  totalMercadoiraaCIVA text NULL,
  dataCarga text NULL,
  totalIVA text NULL,
  rHoraCarga text NULL,
  subTotal text NULL,
  IRSIncidencia text NULL,
  viatura text NULL,
  IRSValorRetido text NULL,
  totalPAgamentos text NULL,
  totalToPay text NULL,
  morada text NULL,
  localidade text NULL,
  cod_postal text NULL,
  subZona text NULL,
  email text NULL,
  telefone text NULL,
  totalLinhas text NULL,
  totalArtigos text NULL,
  totalQtd text NULL,
  IVACodTaxa1 text NULL,
  IVACodTaxa2 text NULL,
  IVACodTaxa3 text NULL,
  IVACodTaxa4 text NULL,
  IVACodTaxa5 text NULL,
  IVACodTaxa6 text NULL,
  IVATaxa1 text NULL,
  IVATaxa2 text NULL,
  IVATaxa3 text NULL,
  IVATaxa4 text NULL,
  IVATaxa5 text NULL,
  IVATaxa6 text NULL,
  IVAIncidencia1 text NULL,
  IVAIncidencia2 text NULL,
  IVAIncidencia3 text NULL,
  IVAIncidencia4 text NULL,
  IVAIncidencia5 text NULL,
  IVAIncidencia6 text NULL,
  IVAValor1 text NULL,
  IVAValor2 text NULL,
  IVAValor3 text NULL,
  IVAValor4 text NULL,
  IVAValor5 text NULL,
  N_CTB text NULL,
  MeioDeExpedicao text NULL,
  Estado_doc text NULL,
  CodRubrica text NULL,
  Descricao_Artigo_L1 text NULL,
  Descricao_Artigo_L2 text NULL,
  Descricao_Artigo_L3 text NULL,
  Descricao_Artigo_L4 text NULL,
  Descricao_Artigo_L5 text NULL,
  SujeitoRetIRS_l1 boolean default false,
  SujeitoRetIRS_l2 boolean default false,
  SujeitoRetIRS_l3 boolean default false,
  SujeitoRetIRS_l4 boolean default false,
  SujeitoRetIRS_l5 boolean default false,
  intNumero text NULL,
  srtNumero text NULL,
  TpMovPagTes text NULL,
 primary key (num_fatura, nif_consumidor, nif_comerciante)
  );
"""

query_tabela_fornecedores = """
CREATE TABLE nif_fornecedores(
  nif INT NOT NULL UNIQUE,
  nome_empresa VARCHAR(255) NOT NULL,
  PRIMARY KEY (nif)
  );
  """

query_tabela_fornecedores_2 = """
CREATE TABLE fornecedor (
  nif varchar(55) not null unique,
  nome varchar(150) not null,
  morada VARCHAR(255) NULL,
  cidade VARCHAR(150) NULL,
  cod_postal VARCHAR(100) NULL,
  cae_rev VARCHAR(20) Null,
  primary key (nif)
  );
  """


def create_fatura_table(db_connection, db_name):
    try:
        execute_query(db_connection, f"use {db_name}")
        execute_query(db_connection, query_tabela)
        execute_query(db_connection, query_tabela_fornecedores)
        execute_query(db_connection, query_tabela_fornecedores_2)
    except Exception as e:
        print("\nNão foi possível criar tabela, ERRO: \n", e)
