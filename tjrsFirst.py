from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
import csv
import codecs

# Configuracoes Gecko Firefox
gecko_driver_path = './geckodriver'
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Initialize the WebDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Main URL
main_url = "https://www.tjrs.jus.br/site_php/precatorios/lista_precatorios_entidades.php?cod_devedor=1&seq=57001&incremento_de_seq=100&entidade=1&nome_entidade=Estado%20do%20Rio%20Grande%20do%20Sul&qtd_precatorios=57079"

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

def extract_precatorio_data(url):
    driver.get(url)
    print(f"Extracting data from: {url}")
    
    data = {
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

    # Extract Parcelas preferenciais information
    parcelas_info = []
    try:
        table = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Parcelas preferenciais')]/following-sibling::table[1]"))
        )
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 4:
                parcelas_info.append({
                    "Posição na fila": cells[0].text,
                    "Tipo Parcela": cells[1].text,
                    "Natureza do Crédito": cells[2].text,
                    "N° Parcela": cells[3].text
                })
    except (TimeoutException, NoSuchElementException):
        print("No Parcelas preferenciais information found or table structure is different.")

    data["Parcelas preferenciais"] = parcelas_info

    return data

# Navigate to the main page
driver.get(main_url)

# Find all precatório links
precatorio_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'precatorio.php')]")
precatorio_urls = [link.get_attribute('href') for link in precatorio_links]

print(f"Found {len(precatorio_urls)} precatório links")

# Extract data from each precatório page
all_data = []
for index, url in enumerate(precatorio_urls, 1):
    print(f"\nProcessing precatório {index} of {len(precatorio_urls)}")
    try:
        data = extract_precatorio_data(url)
        all_data.append(data)
        print(f"Successfully extracted data for {url}")
        time.sleep(1)  # Reduced delay to 1 second
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Save data to CSV

csv_filename = 'precatorios_data.csv'
with codecs.open(csv_filename, 'w', encoding='utf-8-sig') as csvfile:
    fieldnames = list(all_data[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in all_data:
        flat_data = data.copy()
        flat_data['Parcelas preferenciais'] = '; '.join([str(p) for p in data['Parcelas preferenciais']])
        writer.writerow(flat_data)


# Close the browser
driver.quit()

print(f"\nData extraction complete. Results saved to {csv_filename}")
print(f"Total precatórios processed: {len(precatorio_urls)}")
print(f"Successfully extracted data for {len(all_data)} precatórios")