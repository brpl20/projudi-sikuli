from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
processos = [
    "0000031-44.2006.8.16.7000",
    "0000050-94.1999.8.16.7000",
    "0000102-17.2004.8.16.7000",
    "0000131-38.2002.8.16.7000",
    "0000120-33.2007.8.16.7000",
    "0000029-40.2007.8.16.7000",
]

# Instanciar Driver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)
print("Iniciando Driver...")

def extract_and_remove_tj_token(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    token = query_params.get('_tj', [None])[0]
    if '_tj' in query_params:
        del query_params['_tj']
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url, token

def slp(seconds):
    time.sleep(seconds)

def wait_for_element(by, value, timeout=10, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            if attempt < retries - 1:
                print(f"Element not found. Retrying... Attempt {attempt + 1}")
                slp(2)
            else:
                print(f"Element not found after {retries} attempts.")
                return None

wait = WebDriverWait(driver, 10)

print("Iniciando Procedimentos...")
driver.get('https://projudi.tjpr.jus.br/projudi/')
slp(2)
driver.switch_to.frame('mainFrame')
slp(2)
login_element = wait_for_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[1]/ul/li[2]/span[2]')
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
    radio_button = wait_for_element(By.XPATH, '//input[@type="radio" and @name="filtroAdvogado" and @value="qualquerAdvogado"]')
    if radio_button:
        radio_button.click()
        slp(2)

    numero_processo_element = wait_for_element(By.XPATH, '//*[@id="numeroProcesso"]')
    if numero_processo_element:
        numero_processo_element.send_keys(processo)
        slp(2)

    search_button = wait_for_element(By.ID, "pesquisar")
    if search_button:
        search_button.click()
        slp(2)

    buscar_numero_processo_por_xpath = wait_for_element(By.XPATH, '/html/body/div[1]/div[2]/form/table[2]/tbody/tr/td[2]/a[1]')
    if buscar_numero_processo_por_xpath:
        buscar_numero_processo_por_xpath.click()
        slp(7)

    print("Go TRU!")
    print(processo)

    # Try to find habilitacaoProvisoriaButton
    habilitacao = wait_for_element(By.ID, "habilitacaoProvisoriaButton", timeout=5, retries=2)
    
    if habilitacao:
        habilitacao.click()
        slp(4)

        chceckbox_habilitacao = wait_for_element(By.XPATH, '//*[@id="termoAceito"]')
        if chceckbox_habilitacao:
            chceckbox_habilitacao.click()
            slp(4)

        habilitacao_salvar_button = wait_for_element(By.ID, "saveButton")
        if habilitacao_salvar_button:
            habilitacao_salvar_button.click()
            slp(3)
    
    # Whether habilitacaoProvisoriaButton was found or not, proceed to export
    export_button_arrow = wait_for_element(By.ID, "btnMenuExportar")
    if export_button_arrow:
        export_button_arrow.click()
        slp(3)

        export_button_full = wait_for_element(By.XPATH,'//*[@id="exportarProcessoButton"][@value="Tudo"]')
        if export_button_full:
            export_button_full.click() 
            slp(40)

        # Wait for the download button to be clickable
        try:
            export_button = WebDriverWait(driver, 90).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "a8k"))
            )
            export_button.click()
            print("Download iniciado.")
            
            # Wait for download to complete (you might need to adjust this based on file size and connection speed)
            slp(15)  # Waiting for 15 seconds, adjust as needed
        except TimeoutException:
            print("O botão de download não ficou clicável após 90 segundos.")

    if a_to_go:
        slp(2)
        first_element = a_to_go[0]
        driver.get(first_element["href"])
    else:
        print("No matching elements found.")

    slp(4)

driver.quit()