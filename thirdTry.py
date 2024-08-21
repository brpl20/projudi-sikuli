from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


# Setup Selenium WebDriver (make sure to use the appropriate driver for your browser)
driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

# Navigate to the website
driver.get("https://your-website-url.com")

# Find all <a> elements
a_elements = driver.find_elements(By.TAG_NAME, "a")

# Process each <a> element
for a in a_elements:
    href = a.get_attribute("href")
    if href:
        # Remove the token from the href
        if href and "buscaProcessosQualquerInstancia" in href:
            clean_href = remove_tj_token(href)

            # Extract the token from the href
            token = extract_tj_token(href)
        
            print("Found matching element:")
            print(f"Original href: {href}")
            print(f"Token: {token}")
        
            # Return the original element and token
            return a, token

            #https://projudi.tjpr.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?_tj=e3c12b3be7b707dd7342a0cd433dc1f0034dab65850076c7

# Close the browser
driver.quit()