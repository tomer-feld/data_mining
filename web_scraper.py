from time import sleep

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Firefox()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"

try:
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())
    sleep(3)
    elements = driver.find_elements_by_tag_name("article")
    soups = []
    for el in elements:
        soups.append(BeautifulSoup(el.get_attribute('innerHTML'), 'lxml'))
    while len(soups) < 20:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        el = driver.find_element_by_tag_name('article')
        # elements.append(el)
        soups.append(BeautifulSoup(el.get_attribute('innerHTML'), 'lxml'))
    for element in soups:
        # print(type(element))
        # print(element.id)
        res = element.find('div', attrs={
            'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
        print(res.get_text())
        # print(element.get_attribute('innerHTML'))
        # print(element.text)
    # while len(elements) < 20:
    #     elements.append(driver.find_element_by_tag_name('article'))
    print(len(soups))
finally:
    # driver.quit()
    pass
