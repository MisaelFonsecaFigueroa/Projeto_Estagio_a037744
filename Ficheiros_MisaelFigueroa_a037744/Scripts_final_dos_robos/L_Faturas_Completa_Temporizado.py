import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time as t
import xlsxwriter
import re
from selenium.webdriver.support.ui import WebDriverWait
import datetime as dt
import calendar as ca
import MySQL_Functions as Mysql
import Fatura_Functions as FatFun

'''Variante do robô das faturas, onde é possível atribuir um intervalo de tempo'''

# Iniciar o Timer
start_time = t.time()


# Seleção de datas: Vai buscar o ano e o mês atual de acordo com o sistema
print("Por favor insira os dados necessários sobre o periodo de tempo da pesquisa:"
      "\nExemplo: Considerando o ultimo mês como Junho(6) do ano de 2022 com uma quantidade de meses igual a três(3)."
      " O algoritmo vai buscar os dados dos últimos 3 meses incluindo\no mês de Junho.")

mes = int(input("\nUltimo mês da pesquisa?(número do mês) "))
ano = int(input("De qual ano? "))
quantidade = int(input("Qual a quantidade de meses de pesquisa que deseja?(valor numérico) "))

cal = ca.Calendar()

# Dados da Base de dados Mãe
database = "efatura"

URL = 'https://faturas.portaldasfinancas.gov.pt/consultarDocumentosAdquirente.action'  # URL do portal das faturas

# Inicializando o browser com configurações personalizadas
web = FatFun.ini_web()

# Variaveis de Login: NIF e Password
DB_CRED = Mysql.create_db_connection(database)

empresas = Mysql.get_credentials(DB_CRED)


# Obter a sequencia dos meses de pesquisa
seq_meses = FatFun.month_sequence_until(mes, ano, quantidade)

# Ciclo para correr todas as empresas
for empresa in empresas:
    # URL do site das finanças, consulta de faturas
    web.get(URL)

    NIF = empresa[0]
    Password = empresa[2]
    print("\n", "=-" * 20)
    print(empresa[1])

    # Inicializar função de Login
    FatFun.login_empresa(NIF, Password)


    # Ciclo para todos os meses necessários
    for month in seq_meses:
        print(f"\n\nPara o mês de {month[1]} de {month[0]}")

        # Verificar se a base de dados do ano existe
        data_db = str(dt.datetime.now().date().replace(year=month[0]).strftime('%Y'))
        db_name = f"efatura_{data_db}"

        try:
            DBServer = Mysql.create_server_connection()
            # e = Mysql.
            query_verify_db = f"SHOW DATABASES LIKE '{db_name}'"
            result = Mysql.read_query(DBServer, query_verify_db)
            if len(result) == 0:
                query_create_db = f"CREATE DATABASE IF NOT EXISTS {db_name}"
                Mysql.execute_query(DBServer, query_create_db)
                Mysql.clone_db(database, db_name)
            DBServer.close()
        except (Exception,):
            pass

        DB = Mysql.create_db_connection(db_name)

        # Icinializar variaveis do ficheiro (Excel e o Sheet) e criar/aplicar configurações nas células
        nomeEmpresa = web.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/p/strong').text
        nome_Empresa = nomeEmpresa.replace(" ", "_")
        data_faturas = str(dt.datetime.now().date().replace(month=month[2], year=month[0]).strftime('%Y-%m'))
        workbook = xlsxwriter.Workbook(f'FATs_{nome_Empresa}_{data_faturas}.xlsx')
        worksheet = workbook.add_worksheet(f'FATs - {data_faturas}')

        # Criar formatos
        boldformat = workbook.add_format({'bold': True})
        cellFormat = workbook.add_format()

        # função para adicionar configurações de estilo nas células
        def format_cell(formatt):
            formatt.set_text_wrap()
            formatt.set_align('center')
            formatt.set_align('vcenter')

        # Aplicar configurações nos formatos
        format_cell(boldformat)
        format_cell(cellFormat)

        # Função que cria as tabelas(header) no ficheiro e ajusta as medidas das células
        def create_tables():  # Criar ficheiro excel e preencher os headers
            worksheet.write('A1', 'Setor', boldformat)
            worksheet.write('B1', 'NIF Consumidor', boldformat)
            worksheet.write('C1', 'Nome Consumidor', boldformat)
            worksheet.write('D1', 'NIF Comerciante', boldformat)
            worksheet.write('E1', 'Nome Comerciante', boldformat)
            worksheet.write('F1', 'Tipo de Fatura', boldformat)
            worksheet.write('G1', 'Nº Fatura', boldformat)
            worksheet.write('H1', 'Registada por', boldformat)
            worksheet.write('I1', 'Situação', boldformat)
            worksheet.write('J1', 'Data de Emissão', boldformat)
            worksheet.write('K1', 'Código Controlo', boldformat)
            worksheet.write('L1', 'Total', boldformat)
            worksheet.write('M1', 'Iva Total', boldformat)
            worksheet.write('N1', 'Base Tributável Total', boldformat)
            worksheet.write('O1', 'Taxa 1', boldformat)
            worksheet.write('P1', 'IVA 1', boldformat)
            worksheet.write('Q1', 'Taxa 2', boldformat)
            worksheet.write('R1', 'IVA 2', boldformat)
            worksheet.write('S1', 'Taxa 3', boldformat)
            worksheet.write('T1', 'IVA 3', boldformat)
            worksheet.write('U1', 'Taxa 4', boldformat)
            worksheet.write('V1', 'IVA 4', boldformat)

            # Ajustar tamanho dos campos
            worksheet.set_column(1, 1, width=12)
            worksheet.set_column(2, 2, width=30)
            worksheet.set_column(3, 3, width=12)
            worksheet.set_column(4, 4, width=35)
            worksheet.set_column(6, 8, width=15)
            worksheet.set_column(9, 22, width=13)


        # Inicializar função que cria as tabelas
        create_tables()

        # Estrutura responsável por buscar as faturas e adiciona-las no excel
        linha = 1  # contador de linhas
        row_index = 2  # linha no ficheiro

        # Ciclo que busca todos os dias de um determinado mês e ano
        for dia in cal.itermonthdays(month[0], month[2]):
            if dia != 0:
                # print(f"Para o dia {dia}...")
                flexData = str(dt.datetime.now().date().replace(
                    day=dia, month=month[2], year=month[0]).strftime('%Y-%m-%d'))

                # Adicionar filtros e pesquisar: (Data flexível que varia os dias do mês)
                WebDriverWait(web, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="dataInicioFilter"]')))
                dataI = web.find_element(By.XPATH, '//*[@id="dataInicioFilter"]')
                dataI.clear()
                dataI.send_keys(flexData)
                dataF = web.find_element(By.XPATH, '//*[@id="dataFimFilter"]')
                dataF.clear()
                dataF.send_keys(flexData)

                BtnFiltrar = web.find_element(By.XPATH, '//*[@id="pesquisar"]')
                web.execute_script("arguments[0].click();", BtnFiltrar)

                # Total de faturas
                try:
                    WebDriverWait(web, 2).until(EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="documentos_info"]/span')))
                    totalFaturas = web.find_element(By.XPATH, '//*[@id="documentos_info"]/span').text
                    totalFatInt = int(re.search(r'\d+', totalFaturas).group())  # Encontrar o valor numérico no texto
                except (Exception, ):
                    totalFatInt = 0
                    continue

                # Variaveis
                linhas = 10
                paginas = int(totalFatInt / linhas)
                resto = int(totalFatInt % linhas)

                if resto != 0:
                    paginas += 1

                # Ciclos para copiar linhas e passar as paginas
                try:
                    for y in range(1, paginas+1):

                        if y == paginas and resto != 0:
                            linhas = resto

                        for x in range(1, linhas+1):

                            # Adicionar campos no ficheiro
                            WebDriverWait(web, 20).until(EC.visibility_of_element_located((
                                By.XPATH, f'//*[@id="documentos"]/tbody/tr[{str(x)}]/td[1]')))
                            setor = web.find_element(By.XPATH, f'//*[@id="documentos"]/tbody/tr[{str(x)}]/td[1]').text
                            worksheet.write('A' + str(row_index), setor, cellFormat)

                            # Buscar o link da fatura para abri-lo numa outra janela
                            fat = web.find_element(By.XPATH, f'//*[@id="documentos"]/tbody/tr[{str(x)}]/td[5]/a')\
                                .get_attribute('href')
                            web.execute_script("window.open('');")
                            web.switch_to.window(web.window_handles[1])
                            web.get(fat)

                            # Buscar as informações dentro das faturas
                            WebDriverWait(web, 20).until(EC.visibility_of_element_located((
                                By.XPATH, '//*[@id="nifAdquirente"]')))
                            nifConsumidor = web.find_element(By.XPATH, '//*[@id="nifAdquirente"]').text
                            worksheet.write('B' + str(row_index), nifConsumidor, cellFormat)

                            nomeConsumidor = web.find_element(By.XPATH, '//*[@id="nomeAdquirente"]').text
                            worksheet.write('C' + str(row_index), nomeConsumidor, cellFormat)

                            nifComerciante = web.find_element(By.XPATH, '//*[@id="nifEmitente"]').text
                            worksheet.write('D' + str(row_index), nifComerciante, cellFormat)

                            nomeComerciante = web.find_element(By.XPATH, '//*[@id="nomeEmitente"]').text
                            nomeComercianteT = nomeComerciante.replace("'", "''")
                            worksheet.write('E' + str(row_index), nomeComercianteT, cellFormat)

                            tipoFatura = web.find_element(By.XPATH, '//*[@id="tipoDocumento"]').text
                            worksheet.write('F' + str(row_index), tipoFatura, cellFormat)

                            numFatura = web.find_element(By.XPATH, '//*[@id="numDocumento"]').text
                            worksheet.write('G' + str(row_index), numFatura, cellFormat)

                            registadaPor = web.find_element(By.XPATH, '//*[@id="registadoPor"]').text
                            worksheet.write('H' + str(row_index), registadaPor, cellFormat)

                            situacao = web.find_element(By.XPATH, '//*[@id="estadoDocumento"]').text
                            worksheet.write('I' + str(row_index), situacao, cellFormat)

                            dataEmissao = web.find_element(By.XPATH, '//*[@id="dataEmissaoEmitenteDesc"]')\
                                .get_attribute("value")
                            worksheet.write('J' + str(row_index), dataEmissao, cellFormat)

                            codControlo = web.find_element(By.XPATH, '//*[@id="hashEmitenteDesc"]')\
                                .get_attribute("value")
                            worksheet.write('K' + str(row_index), codControlo, cellFormat)

                            totalT = web.find_element(By.XPATH, '//*[@id="valorTotalEmitenteView"]')\
                                .get_attribute("value")
                            worksheet.write('L' + str(row_index), totalT, cellFormat)

                            ivaTotal = web.find_element(By.XPATH, '//*[@id="valorIvaEmitenteView"]')\
                                .get_attribute("value")
                            worksheet.write('M' + str(row_index), ivaTotal, cellFormat)

                            baseTributavelTotal = web\
                                .find_element(By.XPATH, '//*[@id="valorBaseTributavelEmitenteView"]')\
                                .get_attribute("value")
                            worksheet.write('N' + str(row_index), baseTributavelTotal, cellFormat)
                            taxa_ex = ""
                            iva = ""
                            taxa_1 = taxa_2 = taxa_3 = taxa_4 = taxa_ex
                            iva_1 = iva_2 = iva_3 = iva_4 = iva

                            # Ciclo para encontrar os possíveis valores do IVA e as Taxas
                            for g in range(1, 5):
                                validatorCounter = 0
                                try:
                                    taxa_ex = web.find_element(
                                        By.XPATH,
                                        f'/html/body/div[1]/div[4]/div[3]/div[1]/div/div/div[1]/'
                                        f'div/div[4]/div/div/table/tbody/tr[{str(g)}]/td[2]')\
                                        .text
                                    taxa = FatFun.validate_tax(taxa_ex)
                                    iva = web.find_element(
                                        By.XPATH,
                                        f'/html/body/div[1]/div[4]/div[3]/div[1]/div/div/'
                                        f'div[1]/div/div[4]/div/div/table/tbody/tr[{str(g)}]/td[3]')\
                                        .text
                                except (Exception, ):
                                    break

                                if g == 1:
                                    worksheet.write('O' + str(row_index), taxa, cellFormat)
                                    worksheet.write('P' + str(row_index), iva, cellFormat)
                                    taxa_1 = taxa
                                    iva_1 = iva
                                elif g == 2:
                                    worksheet.write('Q' + str(row_index), taxa, cellFormat)
                                    worksheet.write('R' + str(row_index), iva, cellFormat)
                                    taxa_2 = taxa
                                    iva_2 = iva
                                elif g == 3:
                                    worksheet.write('S' + str(row_index), taxa, cellFormat)
                                    worksheet.write('T' + str(row_index), iva, cellFormat)
                                    taxa_3 = taxa
                                    iva_3 = iva
                                elif g == 4:
                                    worksheet.write('U' + str(row_index), taxa, cellFormat)
                                    worksheet.write('V' + str(row_index), iva, cellFormat)
                                    taxa_4 = taxa
                                    iva_4 = iva

                            row_index += 1  # adiciona mais uma linha no ficheiro
                            # Adicionar a fatura na base de dados
                            queryAddFatura = f"insert into fatura values ('{numFatura}', '{setor}'," \
                                             f" '{nifConsumidor}', '{nomeConsumidor}', '{nifComerciante}'," \
                                             f" '{nomeComercianteT}', '{tipoFatura}', '{registadaPor}'," \
                                             f" '{situacao}', '{dataEmissao}', '{codControlo}'," \
                                             f" '{totalT}', '{ivaTotal}', '{baseTributavelTotal}'," \
                                             f" '{taxa_1}', '{iva_1}'," \
                                             f" '{taxa_2}', '{iva_2}', '{taxa_3}', '{iva_3}'," \
                                             f" '{taxa_4}', '{iva_4}');"

                            execute = Mysql.execute_query(DB, queryAddFatura)
                            web.close()  # fecha a aba atual
                            web.switch_to.window(web.window_handles[0])  # Mudar para a aba principal

                            print(f"\rFatura - {linha} - {execute}", end="")
                            # print(" | ", queryAddFatura)
                            # print(codControlo, dataEmissao)  # print para testes
                            linha += 1

                        # Apertar no botão "Próximo", caso existam mais de 10 faturas
                        if totalFatInt > 10:
                            try:
                                text = web.find_element(
                                    By.XPATH, '//*[@id="documentos_paginate"]/ul/li[@class="next"]/a').text
                                btn = web.find_element(By.LINK_TEXT, text)
                                web.execute_script("arguments[0].click();", btn)
                            except (Exception, ):
                                continue

                except Exception as e2:
                    print("Aconteceu algum erro ao tentar adicionar as faturas!\nERRO: ")
                    print(e2)

        # Fechar e guardar o ficheiro
        try:
            workbook.close()
        except (Exception, ):
            print("\n", traceback.format_exc())
            print("Não foi possível guardar o ficheiro!")
            pass
    btn_logout = web.find_element(By.XPATH, '//*[@id="wrapper"]/header/nav/div/div/a')
    web.execute_script("arguments[0].click();", btn_logout)
    # web.close()  # Fechar a janela web caso a UI estiver ligada

    '''# Abrir o ficheiro excel diretamente
    if os.path.exists(f'FATs_{nome_Empresa}_{data_faturas}.xlsx'):  # Verificar se existe na pasta
        print(f"\nAbrindo o ficheiro FATs_{nome_Empresa}_{data_faturas}.xlsx...")
        os.system(f"start EXCEL.EXE FATs_{nome_Empresa}_{data_faturas}.xlsx")  # Abrir o ficheiro
    else:
        print("\nO ficheiro excel não existe!")
    print("=-" * 20)'''

# Terminar o Timer
end_time = t.time()
time_lapsed = end_time - start_time
FatFun.time_convert(time_lapsed)
