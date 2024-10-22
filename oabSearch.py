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

# Configuracoes Gecko Firefox
gecko_driver_path = './geckodriver'
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)
options.add_argument("-headless")  # Make it headless

def get_firefox_driver():
    service = Service(executable_path=gecko_driver_path)
    return webdriver.Firefox(service=service, options=options)

def get_initial_cookies():
    driver = get_firefox_driver()
    try:
        print("Visiting initial page to get cookies...")
        driver.get("https://cna.oab.org.br/")
        time.sleep(5)  # Wait for page to load

        cookies = driver.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        
        token_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
        )
        token = token_element.get_attribute("value")
        
        print("Cookies and token obtained successfully")
        return cookie_dict, token
    finally:
        driver.quit()

def search_lawyer(name=None, insc=None, state=None, cookies=None, token=None):
    print(cookies)
    search_url = "https://cna.oab.org.br/Home/Search"
    search_data = {
        "__RequestVerificationToken": token,
        "IsMobile": "false",
        "NomeAdvo": name,
        "Insc": "",
        "Uf": "",
        "TipoInsc": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    
    print(f"Searching for lawyer: {name}")
    response = requests.post(search_url, json=search_data, headers=headers, cookies=cookies)
    time.sleep(5)  # Wait for 5 seconds
    search_result = response.json()
    print(search_result)
    
    if search_result['Success'] and search_result['Data']:
        detail_url = "https://cna.oab.org.br" + search_result['Data'][0]['DetailUrl']
        detail_response = requests.get(detail_url, headers=headers, cookies=cookies)
        detail_result = detail_response.json()
        
        if detail_result['Success'] and 'DetailUrl' in detail_result['Data']:
            image_url = "https://cna.oab.org.br" + detail_result['Data']['DetailUrl']
            image_response = requests.get(image_url, headers=headers, cookies=cookies)
            print(image_url)
            
            
            if image_response.status_code == 200:
                # Create a safe filename
                safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                filename = f"lawyer_image_{safe_name}.jpg"
                with open(filename, "wb") as f:
                    f.write(image_response.content)
                print(f"Image for {name} downloaded successfully as {filename}")
            else:
                print(f"Failed to download image for {name}. Status code: {image_response.status_code}")
        else:
            print(f"Failed to get image URL for {name}")
    else:
        print(f"Search failed or no results found for {name}")

def main():
    cookies, token = get_initial_cookies()
    
    lawyers = [
        "eduardo walber"
        # Add more lawyers here
    ]
    
    for lawyer in lawyers:
        search_lawyer(lawyer, cookies, token)
        time.sleep(2)  # Small delay between requests

if __name__ == "__main__":
    main()