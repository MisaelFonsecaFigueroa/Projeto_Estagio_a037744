from selenium.webdriver.common.service import Service
import sys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from pyVies import api

'''Última versão do script que contêm as funções que o robô dos fornecedores utiliza'''


def ini_web():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Desativar UI
        options.add_argument("--start-maximized")  # Maximizar janela caso a UI esteja ativa
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"C:\pythonProject.rpa\downloads\\",
                 "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)   # prefs para alterar o diretorio dos downloads

        # definir o chromedrive como um serviço
        s = Service(r"C:\Users\misae\PycharmProjects\Final_scripts\chromedriver.exe")
        web = Chrome(service=s, options=options)
        return web
    except Exception as ex:
        print("Ocorreu um erro ao inicializar o browser!")
        print(ex)
        sys.exit(1)


def find_cae_of(web, nif, iscookies):
    cae_rev_3 = None
    cae_not_found = False
    # Tentativa de inicializar o browser
    try:
        # Pagina web para pesquisa de CAE
        web.get('https://webinq.ine.pt/public/pages/QUERYCAE')
    except Exception as ex:
        print("Ocorreu um erro ao tentar iniciar o browser!")
        print(ex)
        sys.exit(1)

    # Tentativa de procurar os dados pelo NIF
    try:
        # Procurar empresa pelo valor do NIF
        WebDriverWait(web, 20).until(ec.visibility_of_element_located(
            (By.NAME, 'ctl00$contentBody$txtNif')))
        web.find_element(By.NAME, 'ctl00$contentBody$txtNif').send_keys(nif)

        if iscookies is not True:
            # Aceitar os Cookies -> Obrigatorio para poder pesquisar
            web.find_element(By.XPATH, '//*[@id="ctl00_cookieDisclaimer"]/div/div[2]/button').click()
        web.find_element(By.XPATH, '//*[@id="ctl00_contentBody_btPesquisar"]').click()
    except Exception as ex2:
        print(f"Ocorreu um erro ao pesquisar pelo NIF: {nif}")
        print(ex2)
        sys.exit(1)

    # Tentativa de guardar os dados
    try:
        # Guardar os Valores do NOME e CAE nas Variaveis Locais
        erro = 0
        cae_not_found = False
        try:
            cae_rev_3 = int(web.find_element(
                By.XPATH, '//*[@id="ctl00_contentBody_divResult"]/table/tbody/tr/td[3]/a').text)
        except (Exception, ):
            erro += 1
            pass
        if erro == 1:
            try:
                WebDriverWait(web, 5).until(
                    ec.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_contentBody_msgResult"]')))
                print(" Este Nif não tem CAE", end="")
                cae_not_found = True
                cae_rev_3 = None
            except Exception as e:
                print("\nERRO: ", e)
                pass
    except (Exception, ):
        if cae_not_found is True:
            pass
        else:
            sys.exit(1)

    # Print das Variaveis NOME e CAE
    cae = cae_rev_3
    return cae


def verify_vies_vat(nif, region):
    try:
        vies = api.Vies()
        result = vies.request(nif, region, extended_info=False)
    except api.ViesValidationError as e:
        print(e)
        result = None
        pass
    except api.ViesHTTPError as e:
        print(e)
        result = None
        pass
    except api.ViesError as e:
        print(e)
        result = None
        pass
    else:
        return result


def __getCount(address):
    address2 = address
    for x in address:
        counts = address.count('%')
        if counts > 2:
            address2 = address.replace(' % ', '', 1)
    return address2


def getAddress(endereco):
    address = __getCount(endereco)
    countI = 0
    morada = ""
    cidade = ""
    cod_postal = ""
    for char in address:
        if countI == 0:
            morada += char
            if (char == "%"):
                countI += 1
        elif countI == 1:
            cidade += char
            if (char == "%"):
                countI += 1
        elif countI == 2:
            cod_postal += char

    cid2 = cidade.replace('%', '').strip()
    morad2 = morada.replace('%', '').strip()
    codPos = cod_postal.strip()

    return morad2, cid2, codPos
