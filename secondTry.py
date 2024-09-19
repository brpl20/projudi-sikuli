from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


import pdb
import time

# Configuracoes Gecko Firefox
gecko_driver_path = './geckodriver'  # Substitua pelo caminho correto
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'  
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Selecionar Processos
processos = ['0006326-22.2024.8.16.0031', '0025095-11.2024.8.16.0021', '0008957-07.2024.8.16.0170', '0026111-97.2024.8.16.0021']
print("Listando Processos...")
print(processos)

# Instanciar Driver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)
print("Iniciando Driver...")

def extract_and_remove_tj_token(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the query parameters
    query_params = parse_qs(parsed_url.query)
    
    # Extract the '_tj' token if it exists
    token = query_params.get('_tj', [None])[0]
    
    # Remove the '_tj' parameter
    if '_tj' in query_params:
        del query_params['_tj']
    
    # Reconstruct the URL without the '_tj' parameter
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    
    return new_url, token

def slp(seconds):
    time.sleep(seconds)

wait = WebDriverWait(driver, 10)



print("Iniciando Procedimentos...")
driver.get('https://projudi.tjpr.jus.br/projudi/')  # Replace with the URL of the page you want to scrape
slp(2)
driver.switch_to.frame('mainFrame')
slp(2)
login_element = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[1]/ul/li[2]/span[2]')
slp(2)
login_element.click()
a_elements = driver.find_elements(By.TAG_NAME, "a")

a_to_go = []
for a in a_elements:
    href = a.get_attribute("href")
    if href and "buscaProcessosQualquerInstancia" in href:
        clean_href, token = extract_and_remove_tj_token(href)
        print("Found matching element:")
        print(f"Original href: {href}")
        print(f"Cleaned href: {clean_href}")
        print(f"Token: {token}")
        a_to_go.append({"element": a, "href": href, "clean_href": clean_href, "token": token})

if a_to_go:
    slp(2)
    first_element = a_to_go[0]
    driver.get(first_element["href"])
else:
    print("No matching elements found.")


slp(2)

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
    print(processo)
    # Processos Externos Que não São do Advogado 
    # Hablitar aqui =--------> 
    
    # habilitacao = driver.find_element(By.ID, "habilitacaoProvisoriaButton")    
    # habilitacao.click()
    # slp(4)

    # chceckbox_habilitacao = driver.find_element(By.XPATH, '//*[@id="termoAceito"]')
    # chceckbox_habilitacao.click()
    # slp(4)

    # habilitacao_salvar_button = driver.find_element(By.ID, "saveButton")
    # habilitacao_salvar_button.click()
    # slp(3)

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

    if a_to_go:
        slp(2)
        first_element = a_to_go[0]
        driver.get(first_element["href"])
    else:
        print("No matching elements found.")

    slp(4)


driver.quit()


# main_frame = wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
# driver.switch_to.frame(main_frame)
# slp(2)
# buscar_pre_element = driver.find_element(By.ID, 'sm-17234898044130527-13')
# hover = ActionChains(driver).move_to_element(buscar_pre_element)
# hover.perform()
# slp(2)
# buscar_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[8]/ul/li[1]/a')
# slp(2)
# buscar_element.click()


