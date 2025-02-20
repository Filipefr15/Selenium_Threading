from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def init_driver(index):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.set_page_load_timeout(15)

    url='https://cvmweb.cvm.gov.br/swb/default.asp?sg_sistema=fundosreg'

    try:
        driver.get(url)
    except TimeoutException:
        print(f"Erro no carregamento da Thread {index+1}, reiniciando...")
        driver.quit()
        return init_driver(index)

    return driver