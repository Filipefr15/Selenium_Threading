import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
#from openpyxl import load_workbook
from init_driver import init_driver
from count_dropdown_itens import count_dropdown_itens
from list_helper import list_pop, list_receiver
from get_daily_data import get_daily_data

# wb = load_workbook('../BD_CADASTRO_NUMERADO_AGO_TESTE.xlsx')
# ws, ws2 = wb['Fundos'], wb['Fundos_Cota']
# lista_cnpj = []

# for row in ws.iter_rows(values_only=True):
#     cnpj = row[1]
#     lista_cnpj.append(cnpj)

# for row in ws2.iter_rows(values_only=True):
#     cnpj = row[1] 
#     lista_cnpj.append(cnpj)

# print("Coleta de CNPJs finalizada")

dados_diarios_list = []

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

        dados_diarios_list.extend(get_daily_data(index, driver, cnpj, stored_name, item_to_finish))

        
    except TimeoutException:
        print(f"Erro na Thread {index+1}")
        driver.quit()
        print(f"Thread {index+1} reiniciando...")
        get_inside(cnpj, index, item_to_finish)
    driver.quit()

list_cnpj_teste = ["58.878.941/0001-02", "36.248.874/0001-00", "51.017.442/0001-81", "57.270.020/0001-08"]
#list_cnpj_teste = ["58.878.941/0001-02"]

threads = []

max_tries = 3

# Criando threads em blocos de 8
for cnpj in list_cnpj_teste:
    print("Coleta tamanho do dropdown iniciada")
    tamanho = count_dropdown_itens(cnpj)
    while tamanho is None and max_tries > 0:
        print("Erro na coleta do tamanho do dropdown, reiniciando...")
        tamanho = count_dropdown_itens(cnpj)
        max_tries -= 1
    print("Tamanho do dropdown coletado com sucesso")
    list_to_finish = list(range(tamanho))
    list_receiver(list_to_finish)
    for index in range(6):
        try:
            var = list_pop()
            thread = threading.Thread(target=get_inside, args=(cnpj, index, var))
            #print(list_to_finish)
            threads.append(thread)
            thread.start()
        except IndexError:
            pass

# Aguardando todas as threads terminarem
for thread in threads:
    thread.join()

print("Todas as Threads foram finalizadas")

import pandas as pd
df = pd.DataFrame(dados_diarios_list)
df['Mês'] = pd.to_datetime(df['Mês'], format='%m/%Y')
df_sorted = df.sort_values(by=['Cnpj'], ignore_index=True)

#isso é necessário para que o excel deixe os valores de datas em formato de data
df_sorted['Mês'] = pd.to_datetime(df_sorted['Mês']).dt.to_period('M')
df_sorted.to_excel('funds.xlsx', index=False)

print(df_sorted)

print("Planilha gerada com sucesso")  