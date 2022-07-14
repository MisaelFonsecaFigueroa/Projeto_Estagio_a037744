from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time as t

navegador = Chrome()
navegador.get('https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login')
navegador.maximize_window()
t.sleep(3)
navegador.find_element(By.XPATH, '//map/area[2]').click()
t.sleep(2)
navegador.find_element(By.NAME, 'ExpressaoPesquisa').send_keys("03768202000176")
t.sleep(0.5)
navegador.find_element(By.XPATH, '//select[2]/option[4]').click()
t.sleep(1)
navegador.find_element(By.CSS_SELECTOR, 'input[type = "submit"]').click()
navegador.quit()