from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.maximize_window()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"
NUM = 90
try:
    driver.get(url)
    sleep(3)

    elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
    soups = set()
    for element in elements:
        soups.add(BeautifulSoup(element.get_attribute('innerHTML'), 'lxml'))
    while len(soups) < NUM:
        height = elements[-1].location
        driver.execute_script(f"window.scrollTo(0,{height['y']})")
        sleep(3)
        elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
        for element in elements:
            soups.add(BeautifulSoup(element.get_attribute('innerHTML'), 'lxml'))
        print(len(soups))

    for soup in soups:
        for s in soup.findAll('div',attrs={'lang': 'en'}):
            print(s.prettify())
    print(len(soups))
finally:
    driver.quit()
    pass
