import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time as t
import os

'''Este script representa a primeira versão da primeiro bot (para buscar as faturas)'''

web = 0

# Remover o ficheiro xlsx caso exista
if os.path.exists('e-fatura.xlsx'):
    os.remove("e-fatura.xlsx")
    print("O ficheiro: e-fatura.xlsx foi removido!")
else:
    print("A verificar se o ficheiro: e-fatura.xlsx existe...")
    print("O ficheiro não existe!")
    print("Continuando...")

# Tentativa de abrir o Browser
try:
    # Inicializando o browser com configurações personalizadas
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Desativar UI
    # options.add_argument("--start-maximized")  # Maximizar janela caso a UI esteja ativa
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": r"C:\Users\misae\PycharmProjects\RPA_testes\\",
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)   # prefs para alterar o diretorio dos downloads

    s = Service("C:/Users/misae/PycharmProjects/RPA_estagio/chromedriver.exe")  # definir o chromedrive como um serviço
    web = Chrome(service=s, options=options)
    # URL do site das finanças, consulta de faturas
    web.get('https://faturas.portaldasfinancas.gov.pt/consultarDocumentosAdquirente.action')
    print("Inicializando o browser...")
    t.sleep(3)
except Exception as ex:
    print("Ocorreu um erro ao tentar abrir o browser!")
    print(ex)


# Variaveis de Login: NIF e Password
NIF = 513790918
Password = "THRT7973UZWD"

# Tentativa de login
try:
    # Preencher campos e fazer Login
    web.find_element(By.XPATH, '//*[@id="username"]').send_keys(NIF)
    web.find_element(By.XPATH, '//*[@id="password-nif"]').send_keys(Password)
    web.find_element(By.XPATH, '//*[@id="sbmtLogin"]').click()
    t.sleep(5)
    print("Login realizado com sucesso!")
except Exception as ex2:
    print("Ocorreu um erro durante a tentativa de login!")
    print(ex2)


# Tentativa de fazer o download do ficheiro.csv
try:
    web.find_element(By.XPATH, '//*[@id="documentos_wrapper"]/div[1]/div[1]/div[2]/button').click()
    t.sleep(5)
    web.quit()
    print("Ficheiro foi descarregado!")
except Exception as ex3:
    print("Ocorreu um erro ao tentar abrir fazer o download do ficheiro.csv")
    print(ex3)

# Tentativa de transformar o ficheiro csv em xlsx
try:
    read_file = pd.read_csv(r"C:\Users\misae\PycharmProjects\RPA_testes\e-fatura.csv", sep=";")
    read_file.to_excel(r'C:/Users/misae/PycharmProjects/RPA_testes/e-fatura.xlsx', index=None, header=True)
    t.sleep(3)
    print("Foi criado o ficheiro xlsx com base no ficheiro csv!")
except Exception as ex4:
    print("Ocorreu um erro ao tentar criar o ficheiro xlsx!")
    print(ex4)


# Vericar a existencia do ficheiro csv e caso exista remove-lo
if os.path.exists("e-fatura.csv"):
    os.remove("e-fatura.csv")
    print("Ficheiro csv foi removido!")
else:
    print("O ficheiro excel não existe!")

# Abrir o ficheiro excel diretamente
if os.path.exists("e-fatura.xlsx"):
    print("Abrindo ficheiro excel...")
    t.sleep(2)
    os.system("start EXCEL.EXE e-fatura.xlsx")

else:
    print("O ficheiro excel não existe!")
