from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from init_driver import init_driver


def count_dropdown_itens(cnpj):
    #inicia o driver (chrome)
    driver = init_driver(0)

    driver.switch_to.default_content()

    #pesquisa e troca para o frame correto
    WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
    )

    #procura pelo local em que o cnpj deve ser inserido
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='txtCNPJNome']"))
    )

    #insere o cnpj e realiza a pesquisa
    search_input.clear()
    search_input.send_keys(cnpj)
    search_input.send_keys(Keys.ENTER)

    #existem 2 possíveis botões para clicar, um para cada tipo de fundo
    #embora para um histórico completo, seja interessante clicar em ambos, nesse caso,
    #estou optando apenas pelo que possui os registros mais atuais,
    #talvez no futuro seja interessante procurar em um e depois em outro
    #para obter um histórico 100% completo
    try:
        find_name_to_store = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='ddlFundos__ctl1_Linkbutton4']"))
        )
    except TimeoutException:
        find_name_to_store = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='ddlFundos__ctl0_lnkbtn1']"))
        )
    find_name_to_store.click()

    driver.switch_to.default_content()

    #pesquisa e troca para o frame correto
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
    )

    #pesquisa e clica no link para acesso aos dados diários
    dados_diarios = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='Hyperlink2']"))
    )
    dados_diarios.click()

    driver.switch_to.default_content()

    #popup aparece apenas em alguns fundos, para informar sobre atualizações, irrelevante
    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert.accept()
    except:
        pass
    
    #pesquisa e troca para o frame correto
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='Main']"))
    )

    #esse é um dropdown com os meses/anos disponíveis para a consulta
    #aqui, coleto o tamanho para retornar, que influenciará na quantidade de threads
    #que serão alocadas na coleta de dados
    dropdown_data_pesquisa = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='ddComptc']"))
    ))

    #estava enfrentando alguns problemas ao tentar retornar diretamente o tamanho do dropdown
    #por exemplo: return int(len(dropdown_data_pesquisa.options)), então optei por armazenar
    #em uma variável e retornar, para evitar problemas;
    #também fecho a página aberta, para evitar sobrecargas no computador
    len_dropdown = len(dropdown_data_pesquisa.options)
    driver.quit()
    return int(len_dropdown)