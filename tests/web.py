import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from shutil import which

# A classe Service é usada para iniciar uma instância do Chrome WebDriver
service1 = Service(executable_path=which('chromedriver'))
service2 = Service(executable_path=which('chromedriver'))

# webdriver.ChromeOptions é usado para definir a preferência para o browser do Chrome
options = webdriver.ChromeOptions()
#faz com que nao abra a página.
options.add_argument("--headless=new")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# basicamente o driver É o google chrome.
driver1 = webdriver.Chrome(service=service1, options=options)
driver2 = webdriver.Chrome(service=service2, options=options)
#o link que será acessado (uau)
url = 'https://cvmweb.cvm.gov.br/SWB/default.asp?sg_sistema=fundosreg'

def get_url(driver, url):
    driver.get(url)
#pega o local do cnpj.    
    inserir_cnpj = driver.find_elements(By.CLASS_NAME, 'txtCNPJNome')
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "frame")))
    driver.switch_to.frame(iframe[1])
#insere o cnpj
    inserir_cnpj = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtCNPJNome"]')))
    inserir_cnpj.clear()
    inserir_cnpj.send_keys("13.077.415/0001-05")
#clica no botão de enviar
    button_continuar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnContinuar"]')))
    button_continuar.click()

    driver.switch_to.default_content()
    frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Main"]')))
    driver.switch_to.frame(frame)

    checking = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ddlFundos__ctl0_lnkbtn1"]')))
    print(checking.text)

    driver.quit()

def get_url2(driver, url):
    driver.get(url)
#pega o local do cnpj.    
    inserir_cnpj = driver.find_elements(By.CLASS_NAME, 'txtCNPJNome')
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "frame")))
    driver.switch_to.frame(iframe[1])
#insere o cnpj
    inserir_cnpj = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtCNPJNome"]')))
    inserir_cnpj.clear()
    inserir_cnpj.send_keys("13.077.418/0001-49")
#clica no botão de enviar
    button_continuar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnContinuar"]')))
    button_continuar.click()

    driver.switch_to.default_content()
    frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Main"]')))
    driver.switch_to.frame(frame)

    checking = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ddlFundos__ctl0_lnkbtn1"]')))
    print(checking.text)

    driver.quit()