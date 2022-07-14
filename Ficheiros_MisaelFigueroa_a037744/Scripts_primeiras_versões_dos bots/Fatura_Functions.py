import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
import time as t
import math

'''Script antigo das funções do bot das faturas'''


# Função para listar meses de pesquisa
def month_sequence_until(ultimo_mes, ultimo_ano, quantidade_mes):
    if quantidade_mes <= 0:
        raise "Quantidade de meses inválida!"
    elif ultimo_mes < 1 or ultimo_mes > 12:
        raise "Mês inválido!"
    elif ultimo_ano <= 0:
        raise "Ano Inválido"

    else:
        meses = ([1, "Janeiro"], [2, "Fevereiro"], [3, "Março"], [4, "Abril"], [5, "Maio"], [6, "Junho"], [7, "Julho"],
                 [8, "Agosto"], [9, "Setembro"], [10, "Outubro"], [11, "Novembro"], [12, "Dezembro"])

        quantidade = quantidade_mes
        mes = meses[ultimo_mes - 1][0]
        index = mes - quantidade + 1
        # print(f"Index 1: {mes} - {quantidade} + 1 = {index}")
        current_year = ultimo_ano
        first_year = current_year

        if index <= 0:
            if index == 0:
                diferenca = 1
                # print("1 if")
            else:
                diferenca = math.ceil(abs(index)/12)
                # print("Else", diferenca)

            mod_index = abs(index) % 12
            if mod_index == 0 and index != 0:
                diferenca += 1
                print("2 if")

            # print("Vou calcular o segundo index")

            multiplo12 = 1
            if quantidade > 12:
                multiplo12 = round(quantidade/12)
                if multiplo12 == 0:
                    multiplo12 = 1
            # print("Multiplo: ", multiplo12)
            index = (12*multiplo12) - quantidade + mes + 1
            # print(f"Index 2: {(12*multiplo12)} - {quantidade} + {mes} + 1 = {index}")
            # print("Vou calcular o primeiro mes")
            firstmes = meses[index - 1][0]
            # print("Diferenca: ", diferenca)
            current_year -= diferenca
            first_year = current_year

        else:
            firstmes = meses[index - 1][0]

        ordem = []
        counter = firstmes

        for x in range(0, quantidade):
            if counter == 13:
                counter = 1
                current_year += 1

            for c in meses:
                if c[0] == counter:
                    temp = []
                    ordem.append(temp)
                    ordem[x].append(current_year)
                    ordem[x].append(c[1])
                    ordem[x].append(c[0])

            counter += 1
        return ordem


'''teste = month_sequence_until(1, 2022, 30)
print(teste)
print(len(teste))'''


# Função para cronometrar o tempo gasto
def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print(f"\nDuração do processo = {int(hours)}h:{int(mins)}m:{sec:.0f}s")


# Função para validar as taxas
def validate_tax(string):
    if string == "%":
        string = "0 %"
        return string
    else:
        string = string
        return string


# Inicializando o browser com configurações personalizadas
def ini_web():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Desativar UI
        options.add_argument("--start-maximized")  # Maximizar janela caso a UI esteja ativa
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"C:\Users\misae\PycharmProjects\RPA_testes\\",
                 "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)   # prefs para alterar o diretorio dos downloads
        # definir o chromedrive como um serviço
        s = Service("C:/Users/misae/PycharmProjects/RPA_estagio/chromedriver.exe")
        web = Chrome(service=s, options=options)
        print("\rInicializando o browser...\n", end="")
        return web
    except Exception as ex:
        print("Ocorreu um erro ao inicializar o browser!")
        print(ex)
        sys.exit(1)


# Função que realiza o login tendo em conta o NIF e a Password da empresa
def login_empresa(nif, password, web):  # Tentativa de login
    try:
        # Preencher campos e fazer Login
        web.find_element(By.XPATH, '//*[@id="username"]').send_keys(nif)
        web.find_element(By.XPATH, '//*[@id="password-nif"]').send_keys(password)
        web.find_element(By.XPATH, '//*[@id="sbmtLogin"]').click()
        WebDriverWait(web, 5).until(EC.visibility_of_element_located((
            By.XPATH, '//*[@id="wrapper"]/header/div[1]/div/div/h1/a')))
        t.sleep(1)
        print("\rLogin realizado com sucesso!\n", end="")
    except Exception as ex2:
        print("Ocorreu um erro durante a tentativa de login!")
        print(ex2)


# função para adicionar configurações de estilo nas células
def format_cell(formatt):
    formatt.set_text_wrap()
    formatt.set_align('center')
    formatt.set_align('vcenter')


# Função que cria as tabelas(header) no ficheiro e ajusta as medidas das células
def create_tables(worksheet, cell_format):  # Criar ficheiro excel e preencher os headers
    worksheet.write('A1', 'Setor', cell_format)
    worksheet.write('B1', 'NIF Consumidor', cell_format)
    worksheet.write('C1', 'Nome Consumidor', cell_format)
    worksheet.write('D1', 'NIF Comerciante', cell_format)
    worksheet.write('E1', 'Nome Comerciante', cell_format)
    worksheet.write('F1', 'Tipo de Fatura', cell_format)
    worksheet.write('G1', 'Nº Fatura', cell_format)
    worksheet.write('H1', 'Registada por', cell_format)
    worksheet.write('I1', 'Situação', cell_format)
    worksheet.write('J1', 'Data de Emissão', cell_format)
    worksheet.write('K1', 'Código Controlo', cell_format)
    worksheet.write('L1', 'Total', cell_format)
    worksheet.write('M1', 'Iva Total', cell_format)
    worksheet.write('N1', 'Base Tributável Total', cell_format)
    worksheet.write('O1', 'Taxa 1', cell_format)
    worksheet.write('P1', 'IVA 1', cell_format)
    worksheet.write('Q1', 'Taxa 2', cell_format)
    worksheet.write('R1', 'IVA 2', cell_format)
    worksheet.write('S1', 'Taxa 3', cell_format)
    worksheet.write('T1', 'IVA 3', cell_format)
    worksheet.write('U1', 'Taxa 4', cell_format)
    worksheet.write('V1', 'IVA 4', cell_format)

    # Ajustar tamanho dos campos
    worksheet.set_column(1, 1, width=12)
    worksheet.set_column(2, 2, width=30)
    worksheet.set_column(3, 3, width=12)
    worksheet.set_column(4, 4, width=35)
    worksheet.set_column(6, 8, width=15)
    worksheet.set_column(9, 22, width=13)
