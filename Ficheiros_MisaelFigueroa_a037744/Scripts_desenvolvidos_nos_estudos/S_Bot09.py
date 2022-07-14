from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time as t
from selenium.webdriver.common.keys import Keys

navegador = Chrome()
navegador.get('https://ferendum.com/pt/')
navegador.maximize_window()

t.sleep(3)

navegador.find_element(By.NAME, 'titulo').send_keys("A automação é uma coisa boa? (Misael02)")
navegador.find_element(By.NAME, 'descripcion').send_keys("Os robôs estão cada vez mais frequentes em nossas vidas..")
navegador.find_element(By.NAME, 'creador').send_keys("Misael curso de RPA com Python")
navegador.find_element(By.CSS_SELECTOR, 'input[type = "email"]').send_keys("misaelito2001@gmail.com")
navegador.find_element(By.ID, 'op1').send_keys("Sim! Ela me ajuda muito...")
navegador.find_element(By.ID, 'op2').send_keys("Não! estou com medo de perder o emprego...")

navegador.find_element(By.NAME, 'config_anonimo').click()
navegador.find_element(By.NAME, 'config_priv_pub').click()
navegador.find_element(By.NAME, 'config_un_solo_voto').click()
navegador.find_element(By.NAME, 'accept_terms_checkbox').click()
t.sleep(0.5)
navegador.find_element(By.CSS_SELECTOR, 'input[value="Criar enquete"]').click()
t.sleep(3)
navegador.find_element(By.NAME, 'crear_votacion').click()
t.sleep(3)
texto = navegador.find_element(By.ID, 'textoACopiar').text
print(texto)
navegador.quit()

