from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 




chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-cookie-encryption")
chrome_options.add_argument("--disable-popup-blocking")

chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)
website = r'https://www.google.com/'
driver.get(website)
time.sleep(0)
# driver.refresh()

search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'q'))
)

text = ''

def tell_me_about(text):
        driver.get(website)
        time.sleep(0)
        # driver.refresh()
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_box.clear()
        search_box.send_keys(text)
        search_box.submit()
        time.sleep(1)
        classes = [ 'hgKElc','VwiC3b','NA6bn','Ab33Nc']
        for i in classes :
            try :
                text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, i))).text
                if text:
                    return text
            except :
                pass
        else :
             return 'details not found'
            



