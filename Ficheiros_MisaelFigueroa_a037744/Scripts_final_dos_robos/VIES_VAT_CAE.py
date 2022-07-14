import sys
import MySQL_Functions as Mysql
import Forncedores_Functions as Ffun

'''Última versão do robô dos fornecedores'''

# Buscar as empresas
DBServer = Mysql.create_server_connection()
try:
    database = "efatura"
    DB_CRED = Mysql.create_db_connection(database)
    empresas = Mysql.get_credentials(DB_CRED)
    print("Ligação com o servidor de Base de dados estabelecida com sucesso!")
except (Exception, ):
    sys.exit(1)

# Verificar a existência da base de dados da empresa
for empresa in empresas:
    DB = 0
    NIF = empresa[0]
    db_name = f"_{NIF}"
    print("\n", "=-" * 20)
    print(empresa[1])

    # Procurar pela base de dados da empresa, caso não exista é criada
    try:
        query_verify_db = f"SHOW DATABASES LIKE '{db_name}'"
        result = Mysql.read_query(DBServer, query_verify_db)
        if len(result) == 0:
            query_create_db = f"CREATE DATABASE IF NOT EXISTS {db_name}"
            Mysql.execute_query(DBServer, query_create_db)
            Mysql.create_fatura_table(DBServer, db_name)
        DB = Mysql.create_db_connection(db_name)
    except (Exception,):
        sys.exit(1)

    # Variaveis
    isCookies = False
    fornecedores_count = 0
    cae = None
    nome_vat = None
    endereco_vat = None

    # Estabelecer conexão com a base de dados para buscar o nif dos fornecedores
    try:
        Fornecedores = Mysql.get_fornecedores(DB)  # lista de fornecedores
        if len(Fornecedores) == 0 or len(Fornecedores) is None:
            print("Não existem fornecedores que precisam ser adicionados!")
            if empresa[0] == empresas[len(empresas) - 1][0]:
                sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

    # Região de pesquisa do Vat
    region = "PT"

    # inicializar o browser para a pesquisa do cae
    web = Ffun.ini_web()
    morada = cidade = codPostal = ""

    # Ciclo para buscar o NIF de cada fornecedor
    for fornecedor in Fornecedores:
        # print(f'\n\nPara o NIF {fornecedor[0]}')
        if fornecedores_count != 0:
            isCookies = True

        # Nif de pesquisa
        nif = str(fornecedor[0])

        try:
            # Verificar o vat
            vies_result = Ffun.verify_vies_vat(nif, region)
            if vies_result is None:
                nome_vat = fornecedor[0]
                endereco_vat = None
            else:
                # Variaveis necessárias para armazenar na base de dados
                nome_vat = str(vies_result['name']).replace("'", "''")
                endereco_vat = str(vies_result['address']).replace('\n', ' % ')
                endereco_vat.replace("'", "''")
                if nome_vat is None or nome_vat == '' or nome_vat == 'None':
                    nome_vat = fornecedor[1]
                    nome_vat.replace("'", "''")
                if endereco_vat is None or endereco_vat == '':
                    endereco_vat = None
                else:
                    moradaT, cidadeT, codPostalT = Ffun.getAddress(endereco_vat)
                    morada = moradaT.replace("'", "''")
                    cidade = cidadeT.replace("'", "''")
                    codPostal = codPostalT.replace("'", "''")

            # Procurar o cae do nif de pesquisa
            cae = str(Ffun.find_cae_of(web, nif, isCookies))
        except Exception as e:
            if cae is None:
                pass
            else:
                print("ERRO:", e)
                sys.exit(1)

        add_suplier = f"insert into fornecedor(nif, nome, morada," \
                      f" cidade, cod_postal, cae_rev) " \
                      f"values('{fornecedor[0]}', '{nome_vat}'," \
                      f" '{morada}', '{cidade}', '{codPostal}', '{cae}');"

        try:
            result = Mysql.execute_query(DB, add_suplier)
        except Exception as e:
            print(e)
            sys.exit(1)

        if result is not None:
            fornecedores_count += 1
            print(f"\rFornecedores adicionados: {fornecedores_count} - {result}", end="")
            Mysql.execute_query(DB, f"Delete from nif_fornecedores where nif = '{fornecedor[0]}'")
        else:
            print(f"\nNão foi possível adicionar fornecedor de nif {fornecedor[0]} | {add_suplier}")

    DB.close()
