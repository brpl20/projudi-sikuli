from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
import json
import os
import csv

# Configuracoes Gecko Firefox
gecko_driver_path = './geckodriver'
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Initialize the WebDriver for the first script
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

def extract_links(url):
    driver.get(url)
    links = []
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'precatorio.php')]"))
        )
        for element in elements:
            href = element.get_attribute('href')
            if href:
                links.append(href)
    except TimeoutException:
        print(f"Timeout while extracting links from {url}")
    return links

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

# Function to process a single URL
def process_url(url):
    driver.get(url)
    
    info = {
        "URL": url,
        "Tipo de Expediente": safe_extract("//td[strong[contains(text(),'Tipo de Expediente')]]/following-sibling::td"),
        "Número do Expediente": safe_extract("//td[strong[contains(text(),'Número do Expediente')]]/following-sibling::td"),
        "Data de Apresentação": safe_extract("//td[strong[contains(text(),'Data de Apresentação')]]/following-sibling::td"),
        "Processo Administrativo": safe_extract("//td[strong[contains(text(),'Processo Administrativo')]]/following-sibling::td"),
        "Valor do Precatório": safe_extract("//td[strong[contains(text(),'Valor do Precatório')]]/following-sibling::td"),
        "Origem": safe_extract("//td[strong[contains(text(),'Origem')]]/following-sibling::td"),
        "Advogado(s)": safe_extract("//td[strong[contains(text(),'Advogado(s)')]]/following-sibling::td"),
        "Objeto": safe_extract("//td[strong[contains(text(),'Objeto')]]/following-sibling::td"),
        "Orçamento Correspondente": safe_extract("//td[strong[contains(text(),'Orçamento Correspondente')]]/following-sibling::td"),
        "Situação Atual": safe_extract("//td[strong[contains(text(),'Situação Atual')]]/following-sibling::td"),
        "Localização": safe_extract("//td[strong[contains(text(),'Localização')]]/following-sibling::td"),
        "Tribunal de Origem": safe_extract("//td[strong[contains(text(),'Tribunal de Origem')]]/following-sibling::td"),
        "Posição na Fila Ordem Cronológica": safe_extract("//td[strong[contains(text(),'Posição na Fila Ordem Cronológica')]]/following-sibling::td")
    }
    
    info['Advogado(s)'] = info['Advogado(s)'].split('<br')[0].strip()
    print(info)
    
    return info

# Functions for the second script (lawyer search)
def get_firefox_driver_headless():
    options_headless = Options()
    options_headless.add_argument("-headless")
    service = Service(executable_path=gecko_driver_path)
    return webdriver.Firefox(service=service, options=options_headless)

def get_initial_cookies():
    driver_headless = get_firefox_driver_headless()
    try:
        print("Visiting initial page to get cookies...")
        driver_headless.get("https://cna.oab.org.br/")
        time.sleep(5)  # Wait for page to load

        cookies = driver_headless.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        
        token_element = WebDriverWait(driver_headless, 7).until(
            EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
        )
        token = token_element.get_attribute("value")
        
        print("Cookies and token obtained successfully")
        return cookie_dict, token
    finally:
        driver_headless.quit()

def search_lawyer(name, cookies, token):
    search_url = "https://cna.oab.org.br/Home/Search"
    search_data = {
        "__RequestVerificationToken": token,
        "IsMobile": "false",
        "NomeAdvo": name,
        "Insc": "",
        "Uf": "",
        "TipoInsc": ""
    }
    print(search_data)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    
    print(f"Searching for lawyer: {name}")
    response = requests.post(search_url, json=search_data, headers=headers, cookies=cookies)
    time.sleep(5)  # Wait for 5 seconds
    search_result = response.json()
    
    if search_result['Success'] and search_result['Data']:
        detail_url = "https://cna.oab.org.br" + search_result['Data'][0]['DetailUrl']
        detail_response = requests.get(detail_url, headers=headers, cookies=cookies)
        detail_result = detail_response.json()
        
        if detail_result['Success'] and 'DetailUrl' in detail_result['Data']:
            image_url = "https://cna.oab.org.br" + detail_result['Data']['DetailUrl']
            image_response = requests.get(image_url, headers=headers, cookies=cookies)
            
            if image_response.status_code == 200:
                # Create a safe filename
                safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                filename = f"lawyer_image_{safe_name}.jpg"
                with open(filename, "wb") as f:
                    f.write(image_response.content)
                print(f"Image for {name} downloaded successfully as {filename}")
                return filename
            else:
                print(f"Failed to download image for {name}. Status code: {image_response.status_code}")
        else:
            print(f"Failed to get image URL for {name}")
    else:
        print(f"Search failed or no results found for {name}")
    return None

# Main execution
def main():
    input_file = 'cleaned_urls.txt'  # Replace with your input file name
    output_file = 'precatorios_info.csv'  # Output CSV file

    # Get cookies and token for lawyer search
    cookies, token = get_initial_cookies()

    with open(input_file, 'r') as file, open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        main_urls = file.readlines()
        fieldnames = ['URL', 'Tipo de Expediente', 'Número do Expediente', 'Data de Apresentação', 'Processo Administrativo', 
                      'Valor do Precatório', 'Origem', 'Advogado(s)', 'Objeto', 'Orçamento Correspondente', 
                      'Situação Atual', 'Localização', 'Tribunal de Origem', 'Posição na Fila Ordem Cronológica',
                      'Lawyer_Image_Filename']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()

        for main_url in main_urls:
            main_url = main_url.strip()  # Remove any whitespace
            print(f"Extracting links from: {main_url}")
            links = extract_links(main_url)
            
            for url in links:
                print(f"Processing URL: {url}")
                info = process_url(url)
                
                # Process only the first lawyer
                lawyer = info['Advogado(s)']
                if lawyer:
                    image_filename = search_lawyer(lawyer, cookies, token)
                    info['Lawyer_Image_Filename'] = image_filename if image_filename else ""
                else:
                    info['Lawyer_Image_Filename'] = ""
                
                csvwriter.writerow(info)
                time.sleep(1)  # Add a small delay between requests

    # Close the browser
    driver.quit()

    print(f"Data has been saved to {output_file}")

if __name__ == "__main__":
    main()