import time
import requests
import os
import boto3
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from requests.exceptions import RequestException

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

def get_initial_cookies(max_retries=3, retry_delay=10):
    for attempt in range(max_retries):
        try:
            driver = get_firefox_driver()
            driver.get("https://cna.oab.org.br/")
            time.sleep(5)  # Wait for page to load

            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            token_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "__RequestVerificationToken"))
            )
            token = token_element.get_attribute("value")
            
            return cookie_dict, token
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise
        finally:
            driver.quit()

def search_lawyer(insc, state, cookies, token, max_retries=3, retry_delay=10):
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
    
    for attempt in range(max_retries):
        try:
            response = requests.post(search_url, json=search_data, headers=headers, cookies=cookies)
            response.raise_for_status()
            search_result = response.json()
            
            if search_result['Success'] and search_result['Data']:
                detail_url = "https://cna.oab.org.br" + search_result['Data'][0]['DetailUrl']
                detail_response = requests.get(detail_url, headers=headers, cookies=cookies)
                detail_response.raise_for_status()
                detail_result = detail_response.json()
                
                if detail_result['Success'] and 'DetailUrl' in detail_result['Data']:
                    image_url = "https://cna.oab.org.br" + detail_result['Data']['DetailUrl']
                    image_response = requests.get(image_url, headers=headers, cookies=cookies)
                    image_response.raise_for_status()
                    
                    filename = f"{state}_{insc}.jpg"
                    s3_client.put_object(Bucket=s3_bucket_name, Key=filename, Body=image_response.content)
                    print(f"Image for {state} {insc} uploaded successfully as {filename}")
                    return True
                else:
                    error_message = f"Failed to get image URL for {state} {insc}"
                    print(error_message)
                    error_log.append(error_message)
            else:
                error_message = f"Search failed or no results found for {state} {insc}"
                print(error_message)
                error_log.append(error_message)
            return False
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                error_message = f"Max retries exceeded for {state} {insc}: {str(e)}"
                print(error_message)
                error_log.append(error_message)
                return False

def main():
    state = 'AL'
    start_num = 22020
    end_num = 1
    
    for insc in range(start_num, end_num, -1):
        cookies, token = get_initial_cookies()
        success = search_lawyer(insc, state, cookies, token)
        if not success:
            # If search failed, try once more with new cookies and token
            cookies, token = get_initial_cookies()
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