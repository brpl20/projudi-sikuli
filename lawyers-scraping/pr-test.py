import time
import requests
import os
import boto3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# AWS S3 Configuration
s3_bucket_name = os.environ.get('S3_BUCKET', 'oabapi')
s3_client = boto3.client('s3')

# Configuracoes Gecko Firefox
options = Options()
options.add_argument("-headless")  # Make it headless

def get_firefox_driver():
    return webdriver.Firefox(options=options)

def get_initial_cookies():
    driver = get_firefox_driver()
    try:
        driver.get("https://cna.oab.org.br/")
        time.sleep(5)  # Wait for page to load

        cookies = driver.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        
        token_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
        )
        token = token_element.get_attribute("value")
        
        return cookie_dict, token
    finally:
        driver.quit()

def search_lawyer(insc, state, cookies, token):
    search_url = "https://cna.oab.org.br/Home/Search"
    search_data = {
        "__RequestVerificationToken": token,
        "IsMobile": "false",
        "NomeAdvo": "",
        "Insc": str(insc),
        "Uf": state,
        "TipoInsc": ""
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Content-Type": "application/json",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    
    response = requests.post(search_url, json=search_data, headers=headers, cookies=cookies)
    search_result = response.json()
    
    if search_result['Success'] and search_result['Data']:
        detail_url = "https://cna.oab.org.br" + search_result['Data'][0]['DetailUrl']
        detail_response = requests.get(detail_url, headers=headers, cookies=cookies)
        detail_result = detail_response.json()
        
        if detail_result['Success'] and 'DetailUrl' in detail_result['Data']:
            image_url = "https://cna.oab.org.br" + detail_result['Data']['DetailUrl']
            image_response = requests.get(image_url, headers=headers, cookies=cookies)
            
            if image_response.status_code == 200:
                filename = f"{state}_{insc}.jpg"
                s3_client.put_object(Bucket=s3_bucket_name, Key=filename, Body=image_response.content)
                print(f"Image for {state} {insc} uploaded successfully as {filename}")
            else:
                print(f"Failed to download image for {state} {insc}. Status code: {image_response.status_code}")
        else:
            print(f"Failed to get image URL for {state} {insc}")
    else:
        print(f"Search failed or no results found for {state} {insc}")

def main():
    cookies, token = get_initial_cookies()
    
    state = 'PR'
    start_num = 126725
    end_num = 120000 
    
    for insc in range(start_num, end_num, -1):
        search_lawyer(insc, state, cookies, token)
        time.sleep(1.13)  # Delay between requests

if __name__ == "__main__":
    main()