from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import pdb
import time

# Gecko
gecko_driver_path = './geckodriver-v0.34.0-linux64/geckodriver'  # Substitua pelo caminho correto
profile_path = '/home/brpl/snap/firefox/common/.mozilla/firefox/xyssuzza.default'  

# Firefox Options
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Driver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

def slp(seconds):
    time.sleep(seconds)

wait = WebDriverWait(driver, 10)


driver.get('https://projudi.tjpr.jus.br/projudi/')  # Replace with the URL of the page you want to scrape
slp(2)
driver.switch_to.frame('mainFrame')
slp(2)
login_element = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[1]/ul/li[2]/span[2]')
slp(2)
login_element.click()
main_frame = wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
driver.switch_to.frame(main_frame)
slp(2)
buscar_pre_element = driver.find_element(By.ID, 'sm-17234898044130527-13')
hover = ActionChains(driver).move_to_element(buscar_pre_element)
hover.perform()
slp(2)
buscar_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[8]/ul/li[1]/a')
slp(2)
buscar_element.click()


