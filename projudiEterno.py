from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pdb
import time

# Caminho para o Gecko Driver (se não estiver no PATH)
gecko_driver_path = './geckodriver-v0.34.0-linux64/geckodriver'  # Substitua pelo caminho correto
profile_path = '/home/brpl/snap/firefox/common/.mozilla/firefox/xyssuzza.default'  

# Opções do Firefox (opcional)
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)  # This is crucial for loading the profile

# Exemplo: Iniciar o Firefox em modo headless (sem interface gráfica)
# Crie um objeto Service (para versões mais recentes do Selenium)
service = Service(executable_path=gecko_driver_path)

# Crie o driver do Firefox
driver = webdriver.Firefox(service=service, options=options)

try:
    while True:
        time.sleep(290)  # Sleep for 4 minutes and 50 seconds
        driver.get(f"https://projudi.tjpr.jus.br/")
        #driver.refresh()
except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    driver.quit()
