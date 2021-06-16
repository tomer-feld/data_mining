from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.maximize_window()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"

try:
    driver.get(url)
    sleep(3)
    elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
    for el in elements:
        bs = BeautifulSoup(el.get_attribute('innerHTML'), 'lxml')
        print(bs.prettify())
    print(len(elements))
finally:
    driver.quit()
    pass
