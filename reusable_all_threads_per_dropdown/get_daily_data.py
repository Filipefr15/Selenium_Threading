from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from list_helper import list_pop, list_is_none, full_list

dados_diarios_list = []

def get_daily_data(index, driver, cnpj, stored_name, item_to_finish):

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
    )

    dropdown_data_pesquisa = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='ddComptc']"))
    ))

    print(f"Thread {index+1} iniciando coleta de dados diários")
    
    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
    )

    dropdown_data_pesquisa = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='ddComptc']"))
    ))
    dropdown_data_pesquisa.select_by_index(item_to_finish)

    name_selected_dropdown = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='ddComptc']"))
    ))
    name_selected_dropdown = name_selected_dropdown.first_selected_option.get_attribute("value")
    
    linhas_tabela = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table[@id='dgDocDiario']//tr[position()>1]"))
    )
    linhas_validas = [linha for linha in linhas_tabela if linha.find_element(By.XPATH, "td[2]").text.strip()] 
    
    if linhas_validas:
        ultima_linha = linhas_validas[-1]
        dados = ultima_linha.find_elements(By.XPATH, "td")
        dados_diarios = {
            "Cnpj": cnpj,
            "Nome": stored_name,
            "Mês": name_selected_dropdown,
            "Dia": dados[0].text.strip(),
            "Quota": dados[1].text.strip(),
            "Patrimônio Líquido": dados[4].text.strip(),
            "Número de Cotistas": dados[6].text.strip(),
        }
        dados_diarios_list.append(dados_diarios)

    print(f"Thread {index+1} finalizou coleta de dados diários")
    if list_is_none():
        print(f"Thread {index+1} finalizada")
        return dados_diarios_list
    else:
        try:
            new_item_to_finish = list_pop()
            print(full_list())
        except IndexError:
            print(f"Thread {index+1} finalizada")
            pass
        print(f"Thread {index+1} reiniciando procura de dados diários")
        get_daily_data(index, driver, cnpj, stored_name, new_item_to_finish)