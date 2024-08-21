from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


import pdb
import time

# Gecko
gecko_driver_path = './geckodriver'  # Substitua pelo caminho correto
profile_path = '/Users/brpl20/Library/Application Support/Firefox/Profiles/5cri1tvj.default-release'  
processos = ['0007984-63.2023.8.16.7000','0008004-54.2023.8.16.7000','0008007-09.2023.8.16.7000','0008009-76.2023.8.16.7000','0008010-61.2023.8.16.7000','0008012-31.2023.8.16.7000','0008187-25.2023.8.16.7000','0008294-69.2023.8.16.7000','0008416-82.2023.8.16.7000','0008433-21.2023.8.16.7000','0009235-19.2023.8.16.7000','0009241-26.2023.8.16.7000','0009242-11.2023.8.16.7000','0009308-88.2023.8.16.7000','0009419-72.2023.8.16.7000','0009483-82.2023.8.16.7000','0009645-77.2023.8.16.7000','0009785-14.2023.8.16.7000','0009795-58.2023.8.16.7000','0009829-33.2023.8.16.7000','0010075-29.2023.8.16.7000','0010205-19.2023.8.16.7000','0010236-39.2023.8.16.7000','0010383-65.2023.8.16.7000','0010577-65.2023.8.16.7000','0010804-55.2023.8.16.7000','0010942-22.2023.8.16.7000','0011174-34.2023.8.16.7000','0011175-19.2023.8.16.7000','0011179-56.2023.8.16.7000','0011180-41.2023.8.16.7000','0011432-44.2023.8.16.7000','0011433-29.2023.8.16.7000','0011439-36.2023.8.16.7000','0011440-21.2023.8.16.7000','0000007-83.2024.8.16.7000','0000142-95.2024.8.16.7000','0000159-34.2024.8.16.7000','0000261-56.2024.8.16.7000','0000283-17.2024.8.16.7000','0000313-52.2024.8.16.7000','0000317-89.2024.8.16.7000','0000318-74.2024.8.16.7000','0000320-44.2024.8.16.7000','0000331-73.2024.8.16.7000','0000337-80.2024.8.16.7000','0000385-39.2024.8.16.7000','0000387-09.2024.8.16.7000','0000389-76.2024.8.16.7000','0000390-61.2024.8.16.7000','0000398-38.2024.8.16.7000','0000399-23.2024.8.16.7000','0000741-34.2024.8.16.7000','0000793-30.2024.8.16.7000','0000794-15.2024.8.16.7000','0000821-95.2024.8.16.7000','0000822-80.2024.8.16.7000','0000823-65.2024.8.16.7000','0000825-35.2024.8.16.7000','0000826-20.2024.8.16.7000','0000827-05.2024.8.16.7000','0000942-26.2024.8.16.7000','0001066-09.2024.8.16.7000','0001155-32.2024.8.16.7000','0001413-42.2024.8.16.7000','0001615-19.2024.8.16.7000','0001620-41.2024.8.16.7000','0001625-63.2024.8.16.7000','0001632-55.2024.8.16.7000','0001661-08.2024.8.16.7000','0001662-90.2024.8.16.7000','0001664-60.2024.8.16.7000','0001665-45.2024.8.16.7000','0001667-15.2024.8.16.7000','0001745-09.2024.8.16.7000','0001894-05.2024.8.16.7000','0002030-02.2024.8.16.7000','0002045-68.2024.8.16.7000','0002048-23.2024.8.16.7000','0002052-60.2024.8.16.7000','0002059-52.2024.8.16.7000','0002093-27.2024.8.16.7000','0002096-79.2024.8.16.7000','0002097-64.2024.8.16.7000','0002105-41.2024.8.16.7000','0002121-92.2024.8.16.7000','0002129-69.2024.8.16.7000','0002218-92.2024.8.16.7000','0002241-38.2024.8.16.7000','0002322-84.2024.8.16.7000','0002454-44.2024.8.16.7000','0002459-66.2024.8.16.7000','0002731-60.2024.8.16.7000','0002738-52.2024.8.16.7000','0002739-37.2024.8.16.7000','0002741-07.2024.8.16.7000','0002742-89.2024.8.16.7000','0002744-59.2024.8.16.7000','0002808-69.2024.8.16.7000','0003001-84.2024.8.16.7000','0003003-54.2024.8.16.7000','0003006-09.2024.8.16.7000','0003007-91.2024.8.16.7000','0003054-65.2024.8.16.7000','0003055-50.2024.8.16.7000','0003309-23.2024.8.16.7000','0003697-23.2024.8.16.7000','0003998-67.2024.8.16.7000','0004001-22.2024.8.16.7000','0004003-89.2024.8.16.7000','0004009-96.2024.8.16.7000','0004010-81.2024.8.16.7000','0004012-51.2024.8.16.7000','0004013-36.2024.8.16.7000','0004017-73.2024.8.16.7000','0004019-43.2024.8.16.7000','0004020-28.2024.8.16.7000','0004025-50.2024.8.16.7000','0004026-35.2024.8.16.7000','0004051-48.2024.8.16.7000','0004054-03.2024.8.16.7000','0004059-25.2024.8.16.7000','0004060-10.2024.8.16.7000','0004063-62.2024.8.16.7000','0004086-08.2024.8.16.7000','0004087-90.2024.8.16.7000','0004102-59.2024.8.16.7000','0004134-64.2024.8.16.7000','0004286-15.2024.8.16.7000','0004301-81.2024.8.16.7000','0004331-19.2024.8.16.7000','0004554-69.2024.8.16.7000','0004590-14.2024.8.16.7000','0004679-37.2024.8.16.7000','0004760-83.2024.8.16.7000','0004761-68.2024.8.16.7000','0004762-53.2024.8.16.7000','0004855-16.2024.8.16.7000','0004863-90.2024.8.16.7000','0004865-60.2024.8.16.7000','0004869-97.2024.8.16.7000','0005065-67.2024.8.16.7000','0005122-85.2024.8.16.7000','0005165-22.2024.8.16.7000','0005209-41.2024.8.16.7000','0005228-47.2024.8.16.7000','0005235-39.2024.8.16.7000','0005247-53.2024.8.16.7000','0005249-23.2024.8.16.7000']
# MANUAL => 0007919-68.2023.8.16.7000
# Firefox Options
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Driver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)


def extract_and_remove_tj_token(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Get the query parameters
    query_params = parse_qs(parsed_url.query)
    
    # Extract the '_tj' token if it exists
    token = query_params.get('_tj', [None])[0]
    
    # Remove the '_tj' parameter
    if '_tj' in query_params:
        del query_params['_tj']
    
    # Reconstruct the URL without the '_tj' parameter
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    
    return new_url, token

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
    # Selecionar "Qualquer Processo"
    radio_button = driver.find_element(By.XPATH, '//input[@type="radio" and @name="filtroAdvogado" and @value="qualquerAdvogado"]')
    radio_button.click()
    slp(2)

    # Digitar Número do Processo 
    numero_processo_element = driver.find_element(By.XPATH, '//*[@id="numeroProcesso"]')
    numero_processo_element.send_keys(processo)
    #slp(2)
    #numero_processo_element.send_keys(Keys.TAB)
    slp(2)
    search_button = driver.find_element(By.ID, "pesquisar")
    search_button.click()
    slp(2)
    buscar_numero_processo_por_xpath = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/form/table[2]/tbody/tr/td[2]/a[1]')
    #pdb.set_trace()
    #buscar_numero_processo_por_xpath.click()
    for element in buscar_numero_processo_por_xpath:
        element.click()
        break
        #print(element)
        #pdb.set_trace()
    slp(7)
    print("Go TRU!")
    print(processo)
    
    habilitacao = driver.find_element(By.ID, "habilitacaoProvisoriaButton")    
    habilitacao.click()
    slp(4)

    chceckbox_habilitacao = driver.find_element(By.XPATH, '//*[@id="termoAceito"]')
    chceckbox_habilitacao.click()
    slp(4)

    habilitacao_salvar_button = driver.find_element(By.ID, "saveButton")
    habilitacao_salvar_button.click()
    slp(3)

    export_button_arrow = driver.find_element(By.ID, "btnMenuExportar")
    export_button_arrow.click()
    slp(3)

    export_button = driver.find_element(By.ID, "exportarProcessoButton")
    #pdb.set_trace()
    export_button_full = driver.find_element(By.XPATH,'//*[@id="exportarProcessoButton"][@value="Tudo"]')
    export_button_full.click() 
    slp(4)

    export_button = driver.find_element(By.CLASS_NAME, "a8k")
    export_button.click() 
    slp(3)

    if a_to_go:
        slp(2)
        first_element = a_to_go[0]
        driver.get(first_element["href"])
    else:
        print("No matching elements found.")

    slp(4)


driver.quit()


# main_frame = wait.until(EC.presence_of_element_located((By.ID, "mainFrame")))
# driver.switch_to.frame(main_frame)
# slp(2)
# buscar_pre_element = driver.find_element(By.ID, 'sm-17234898044130527-13')
# hover = ActionChains(driver).move_to_element(buscar_pre_element)
# hover.perform()
# slp(2)
# buscar_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/ul/li[8]/ul/li[1]/a')
# slp(2)
# buscar_element.click()


