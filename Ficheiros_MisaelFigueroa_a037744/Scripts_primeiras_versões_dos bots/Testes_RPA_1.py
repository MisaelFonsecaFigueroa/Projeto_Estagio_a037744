from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time as t
import os
import xlsxwriter
import re
from selenium.webdriver.support.ui import WebDriverWait
import datetime as dt
import calendar as ca

'''Outro script para testes'''

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Desativar UI
options.add_argument("--start-maximized")  # Maximizar janela caso a UI esteja ativa
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": r"C:\Users\misae\PycharmProjects\RPA_testes\\",
         "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)   # prefs para alterar o diretorio dos downloads

s = Service("C:/Users/misae/PycharmProjects/RPA_estagio/chromedriver.exe")  # definir o chromedrive como um serviço
web = Chrome(service=s, options=options)
# URL do site das finanças, consulta de faturas
web.get('https://faturas.portaldasfinancas.gov.pt/consultarDocumentosAdquirente.action')
print("Inicializando o browser...")

NIF = 0
Password = ""

try:
    # Preencher campos e fazer Login
    web.find_element(By.XPATH, '//*[@id="username"]').send_keys(NIF)
    web.find_element(By.XPATH, '//*[@id="password-nif"]').send_keys(Password)
    web.find_element(By.XPATH, '//*[@id="sbmtLogin"]').click()
    t.sleep(2)
    print("Login realizado com sucesso!")
except Exception as ex2:
    print("Ocorreu um erro durante a tentativa de login!")
    print(ex2)

'''f = web.find_element(By.XPATH, '//*[@id="documentos"]/tbody/tr[1]/td[5]/a').get_attribute('href')
web.execute_script("window.open('');")
web.switch_to.window(web.window_handles[1])
web.get(f)
web.close()
web.switch_to.window(web.window_handles[0])
web.close()'''
t.sleep(2)
print("Vou apertar")
WebDriverWait(web, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                         '//*[@id="documentos_paginate"]/ul/li[@class="next"]/a')))
text = "Próximos →"
print(f"2 {text} 2")
btn = web.find_element(By.LINK_TEXT, text)
web.execute_script("arguments[0].click();", btn)
print("apertei")
