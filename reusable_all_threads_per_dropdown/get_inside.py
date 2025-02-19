from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from init_driver import init_driver

def get_inside(cnpj, index, item_to_finish):
    try:
        print(f"Thread {index+1} iniciada para o CNPJ {cnpj}")
        driver = init_driver(index)
        print(f"Driver da Thread {index+1} iniciado com sucesso")

        #pesquisa e troca para o frame correto sem precisar declarar uma variável nova no processo
        WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
        )

        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='txtCNPJNome']"))
        )

        search_input.clear()
        
        search_input.send_keys(cnpj)
        search_input.send_keys(Keys.ENTER)
        print(f"Thread {index+1} pesquisou o CNPJ {cnpj}")

        try:
            find_name_to_store = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//a[@id='ddlFundos__ctl1_Linkbutton4']"))
            )
        except TimeoutException:
            find_name_to_store = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@id='ddlFundos__ctl0_lnkbtn1']"))
            )

        stored_name = find_name_to_store.text
        find_name_to_store.click()

        driver.switch_to.default_content()

        #pesquisa e troca para o frame correto sem precisar declarar uma variável nova no processo
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
        )

        dados_diarios = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='Hyperlink2']"))
        )
        dados_diarios.click()
        print(f"Thread {index+1} clicou em dados diários")

        driver.switch_to.default_content()

        #pop-up com mensagem irrelevante aparece e precisa ser fechado.
        try:
            alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert.accept()
        except:
            pass

        get_dados_diarios(index, driver, cnpj, stored_name, item_to_finish)

        
    except TimeoutException:
        print(f"Erro na Thread {index+1}")
        driver.quit()
        print(f"Thread {index+1} reiniciando...")
        get_inside(cnpj, index, item_to_finish)
    driver.quit()