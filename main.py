from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import logging
import time

chrome_options = Options()

chrome_options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

driver.get("https://www.biopharmcatalyst.com/auth/google/redirect")

email = driver.find_element(by=By.CSS_SELECTOR, value="input[type=email][autocomplete=username]")
email.send_keys()


upcoming = set()

'''
for x in range(10):
    query = "html body #app main div div section div div:nth-of-type(3) div:nth-of-type(2) div div table tbody tr:nth-of-type(" + str(x + 1) + ")"
    ticker = driver.find_element(by=By.CSS_SELECTOR, value=query + " td div")
    ticker = ticker.get_attribute("blurred-text")
    date = driver.find_element(by=By.CSS_SELECTOR, value=query + " td:nth-of-type(8) div")
    date = date.get_attribute("blurred-text")
    print(date)
    cat = (ticker, date)
    upcoming.add(cat)
'''

time.sleep(1000)

driver.quit()

