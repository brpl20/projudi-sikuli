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
# "0081959-66.2019.8.16.0014",
# "0029174-79.2017.8.16.0182",
# "0004011-68.2020.8.16.0190",
# "0001205-41.2017.8.16.0004",
# /html/body/div[1]/div[2]/form/fieldset/table[3]/tbody/tr[1]/td/div/ul/li[3]/div[2]/a
processos = [
"0018820-92.2017.8.16.0182",
"0007590-58.2019.8.16.0190",

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
        slp(2)

    print("Go TRU!")
    print(processo)

    dados = wait_for_element(By.XPATH, '/html/body/div[1]/div[2]/form/fieldset/table[3]/tbody/tr[1]/td/div/ul/li[3]/div[2]/a', timeout=1, retries=3)
    dados.click()

    buscar_adv = wait_for_element(By.XPATH, 'resultTable', timeout=2, retries=2)
    slp(2)
    # buscar_adv_name = wait_for_element(By.XPATH, "//td[5]/following-sibling::td/ul/li", timeout=2, retries=2.text.strip())
    lawyer_elements = driver.find_elements(By.XPATH, "//td[5]/following-sibling::td/ul/li")
    lawyer_names = [lawyer.text.strip() for lawyer in lawyer_elements]
    
    # Print the extracted lawyer's name
    
    
    
    plus_button = wait_for_element(By.XPATH, ' //*[@id="iconpromoventes0"]', timeout=1, retries=3)
    plus_button.click()
    slp(2)
    
    
    
    link_autor = wait_for_element(By.XPATH, "//a[contains(@href, 'parteProcesso')]", timeout=2, retries=2)
    link_autor.click()
    slp(2)
    
    form = wait_for_element(By.CLASS_NAME, "form", timeout=2, retries=3)

    # Extract Nome
    nome = wait_for_element(By.XPATH, "//td[label[text()='Nome:']]/following-sibling::td", timeout=2, retries=2).text.strip()

    # Extract CPF
    cpf = wait_for_element(By.XPATH, "//td[label[text()='CPF/CNPJ:']]/following-sibling::td", timeout=2, retries=2).text.strip()

    # Extract Data de Nascimento
    data_nascimento = wait_for_element(By.XPATH, "//td[label[text()='Data de Nascimento:']]/following-sibling::td", timeout=2, retries=2).text.strip()

    # Print the extracted information
    print("Nome:", nome)
    print("CPF:", cpf)
    print("Data de Nascimento:", data_nascimento)
    print("Lawyer(s) Name(s):")
    for name in lawyer_names:
        print(name)
    
    driver.quit()
