from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time

# Configuracoes Gecko Firefox
gecko_driver_path = './geckodriver'
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Initialize the WebDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)
url = "https://www.tjrs.jus.br/site_php/precatorios/precatorio.php?Numero_Informado=250097&tipo_pesquisa=por_precatorio&aba_opcao_consulta="

driver.get(url)

# Function to safely extract text using XPath
def safe_extract(xpath, retries=3, delay=0.5):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text.strip()
        except (TimeoutException, NoSuchElementException):
            time.sleep(delay)
    return "Not found"

# Extract main information
info = {
    "Tipo de Expediente": safe_extract("//td[strong[contains(text(),'Tipo de Expediente')]]/following-sibling::td"),
    "Data de Apresentação": safe_extract("//td[strong[contains(text(),'Data de Apresentação')]]/following-sibling::td"),
    "Processo Administrativo": safe_extract("//td[strong[contains(text(),'Processo Administrativo')]]/following-sibling::td"),
    "Valor do Precatório": safe_extract("//td[strong[contains(text(),'Valor do Precatório')]]/following-sibling::td"),
    "Advogado(s)": safe_extract("//td[strong[contains(text(),'Advogado(s)')]]/following-sibling::td"),
    "Objeto": safe_extract("//td[strong[contains(text(),'Objeto')]]/following-sibling::td"),
    "Orçamento Correspondente": safe_extract("//td[strong[contains(text(),'Orçamento Correspondente')]]/following-sibling::td"),
    "Situação Atual": safe_extract("//td[strong[contains(text(),'Situação Atual')]]/following-sibling::td"),
    "Localização": safe_extract("//td[strong[contains(text(),'Localização')]]/following-sibling::td"),
    "Tribunal de Origem": safe_extract("//td[strong[contains(text(),'Tribunal de Origem')]]/following-sibling::td"),
    "Posição na Fila Ordem Cronológica": safe_extract("//td[strong[contains(text(),'Posição na Fila Ordem Cronológica')]]/following-sibling::td")
}

# Print extracted main information
print("Main Information:")
for key, value in info.items():
    print(f"{key}: {value}")

# Extract Parcelas preferenciais information
print("\nParcelas preferenciais deferidas:")

try:
    table = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Parcelas preferenciais')]/following-sibling::table[1]"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
    
    if rows:
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 4:
                print(f"Posição na fila: {cells[0].text}")
                print(f"Tipo Parcela: {cells[1].text}")
                print(f"Natureza do Crédito: {cells[2].text}")
                print(f"N° Parcela: {cells[3].text}")
                print("---")
    else:
        print("No Parcelas preferenciais information found.")
except (TimeoutException, NoSuchElementException):
    print("No Parcelas preferenciais information found or table structure is different.")

# Close the browser
driver.quit()