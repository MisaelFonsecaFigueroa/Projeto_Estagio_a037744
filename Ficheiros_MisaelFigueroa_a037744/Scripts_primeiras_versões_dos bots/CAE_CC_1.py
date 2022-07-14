from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time as t
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service


'''Este script representa a primeira versão da função de buscar o valor do CAE de uma empresa'''

print("Aguarde um momento...")

# Adicionar opcao de desativar UI
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

NIF = 0  # NIF da empresa
web = 0
nome = ""
cae_rev_3 = ""

# Tentativa de inicializar o browser
try:
    # Inicializar o browser e entrar no link
    s = Service("C:/Users/misae/PycharmProjects/RPA_estagio/chromedriver.exe")
    web = Chrome(options=options)
    web.get('https://webinq.ine.pt/public/pages/QUERYCAE')  # Pagina web para pesquisa de CAE
    web.maximize_window()
    t.sleep(5)
except Exception as ex:
    print("Ocorreu um erro ao tentar iniciar o browser!")
    print(ex)

# Tentativa de procurar os dados pelo NIF
try:
    # Procurar empresa pelo valor do NIF
    web.find_element(By.NAME, 'ctl00$contentBody$txtNif').send_keys(NIF)
    # Aceitar os Cookies -> Obrigatorio para poder pesquisar
    web.find_element(By.XPATH, '//*[@id="ctl00_cookieDisclaimer"]/div/div[2]/button').click()
    web.find_element(By.XPATH, '//*[@id="ctl00_contentBody_btPesquisar"]').click()
    t.sleep(3)
except Exception as ex2:
    print(f"Ocorreu um erro ao pesquisar pelo NIF: {NIF}")
    print(ex2)

# Tentativa de guardar os dados
try:
    # Guardar os Valores do NOME e CAE nas Variaveis Locais
    cae_rev_3 = int(web.find_element(By.XPATH, '//*[@id="ctl00_contentBody_divResult"]/table/tbody/tr/td[3]/a').text)
    nome = web.find_element(By.XPATH, '//*[@id="ctl00_contentBody_divResult"]/table/tbody/tr/td[2]').text
except Exception as ex3:
    print("Ocorreu um erro ao tentar guardar os dados!")
    print(ex3)

web.quit()

# Print das Variaveis NOME e CAE
print("=-"*20)
print(f"Para o NIF {NIF}:\nNome: {nome} | CAE_REV_3: {cae_rev_3}")
print("=-"*20)
