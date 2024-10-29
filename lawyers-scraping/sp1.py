import time
import requests
import os
import boto3
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
s3_bucket_name = os.getenv('S3_BUCKET')
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-west-2'
)

# Configuracoes Gecko Firefox
options = Options()
options.add_argument("-headless")  # Make it headless

# Initialize error log
error_log = []

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
                error_message = f"Failed to download image for {state} {insc}. Status code: {image_response.status_code}"
                print(error_message)
                error_log.append(error_message)
        else:
            error_message = f"Failed to get image URL for {state} {insc}"
            print(error_message)
            error_log.append(error_message)
    else:
        error_message = f"Search failed or no results found for {state} {insc}"
        print(error_message)
        error_log.append(error_message)

def main():
    cookies, token = get_initial_cookies()
    
    state = 'SP'
    start_num = 521999
    end_num = 417001
    
    for insc in range(start_num, end_num, -1):
        search_lawyer(insc, state, cookies, token)
        time.sleep(1.13)  # Delay between requests

    # After the loop, write errors to a file and upload to S3
    if error_log:
        error_file_name = f"error_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_file_name, 'w') as f:
            for error in error_log:
                f.write(f"{error}\n")
        
        # Upload error log to S3
        with open(error_file_name, 'rb') as f:
            s3_client.put_object(Bucket=s3_bucket_name, Key=f"error_logs/{error_file_name}", Body=f)
        
        print(f"Error log uploaded to S3 as {error_file_name}")
        
        # Remove local error log file
        os.remove(error_file_name)

if __name__ == "__main__":
    main()