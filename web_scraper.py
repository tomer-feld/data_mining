from time import sleep

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
PATH = 'C:\\Users\\tomer\\chromedriver.exe'
driver = webdriver.Chrome(PATH)
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"

try:
    driver.get(url)
    source = driver.page_source
    print(type(source))
    soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())
    sleep(5)
    elements = driver.find_elements_by_tag_name("article")
    for element in elements:
        soup = BeautifulSoup(element.get_attribute('innerHTML'), 'lxml')
        res  = soup.find('div', attrs={'class':'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
        print(res.get_text())
        # print(element.text)
finally:
    # driver.quit()
    pass
