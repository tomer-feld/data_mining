from time import sleep

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
# PATH = 'C:\\Users\\tomer\\chromedriver.exe'
driver = webdriver.Firefox()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"

try:
    driver.get(url)
    source = driver.page_source
    # print(type(source))
    soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())
    sleep(3)
    elements = driver.find_elements_by_tag_name("article")
    for element in elements:
        # print(type(element))
        # print(element.id)
        el = element.get_attribute('innerHTML')
        souper = BeautifulSoup(el, 'lxml')
        print(souper.prettify())
        # print(element.get_attribute('innerHTML'))
        # print(element.text)
    print(len(elements))
finally:
    driver.quit()
    pass
