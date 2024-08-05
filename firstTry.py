from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import pdb
import time


# Caminho para o Gecko Driver (se não estiver no PATH)
gecko_driver_path = './geckodriver-v0.34.0-linux64/geckodriver'  # Substitua pelo caminho correto
profile_path = '/home/brpl/snap/firefox/common/.mozilla/firefox/xyssuzza.default'  

# Opções do Firefox (opcional)
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)  # Perfil do Firefox 

# Exemplo: Iniciar o Firefox em modo headless (sem interface gráfica)
# Crie um objeto Service (para versões mais recentes do Selenium)
service = Service(executable_path=gecko_driver_path)

# Crie o driver do Firefox
driver = webdriver.Firefox(service=service, options=options)

# Navegue para uma página
#driver.add_cookie({'name' : 'projudi', 'value' : 'bar', 'path' : './cookies-projudi-tjpr-jus-br.txt'})
#driver.add_cookie({'name' : 'tjpr', 'value' : 'bar', 'path' : './cookies-tjpr-jus-br.txt'})

def slp(seconds):
    time.sleep(seconds)

slp(4)
token = ''
driver.get(f"https://projudi.tjpr.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?_tj={token}")
slp(4)

processos =  [] 



for processo in processos:
    # Selecionar "Qualquer Processo"
    radio_button = driver.find_element(By.XPATH, '//input[@type="radio" and @name="filtroAdvogado" and @value="qualquerAdvogado"]')
    radio_button.click()
    slp(2)

    # Digitar Número do Processo 
    numero_processo_element = driver.find_element(By.XPATH, '//*[@id="numeroProcesso"]')
    numero_processo_element.send_keys(processo)
    #slp(2)
    #numero_processo_element.send_keys(Keys.TAB)
    slp(2)
    search_button = driver.find_element(By.ID, "pesquisar")
    search_button.click()
    slp(2)
    buscar_numero_processo_por_xpath = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/form/table[2]/tbody/tr/td[2]/a[1]')
    #pdb.set_trace()
    #buscar_numero_processo_por_xpath.click()
    for element in buscar_numero_processo_por_xpath:
        element.click()
        break
        #print(element)
        #pdb.set_trace()
    slp(7)
    print("Go TRU!")
    
    habilitacao = driver.find_element(By.ID, "habilitacaoProvisoriaButton")    
    habilitacao.click()
    slp(4)

    chceckbox_habilitacao = driver.find_element(By.XPATH, '//*[@id="termoAceito"]')
    chceckbox_habilitacao.click()
    slp(4)

    habilitacao_salvar_button = driver.find_element(By.ID, "saveButton")
    habilitacao_salvar_button.click()
    slp(3)

    export_button_arrow = driver.find_element(By.ID, "btnMenuExportar")
    export_button_arrow.click()
    slp(3)

    export_button = driver.find_element(By.ID, "exportarProcessoButton")
    #pdb.set_trace()
    export_button_full = driver.find_element(By.XPATH,'//*[@id="exportarProcessoButton"][@value="Tudo"]')
    export_button_full.click() 
    slp(4)

    export_button = driver.find_element(By.CLASS_NAME, "a8k")
    export_button.click() 
    slp(3)

    driver.get(f"https://projudi.tjpr.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?_tj={token}")
    slp(4)





driver.quit()


