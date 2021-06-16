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
    sleep(5)
    elements = driver.find_elements_by_tag_name("article")
    for element in elements:
        soup = BeautifulSoup(element.get_attribute('innerHTML'), 'lxml')
        # print(soup.prettify())

        tweet_text = soup.find('div', attrs={
            'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
        print('Tweet: ', tweet_text.get_text())
        if soup.find(text='Quote Tweet'):
            retweet_text = soup.find('div', attrs={
                'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0'})

        tweet_numbers = soup.findAll('div', attrs={'class': 'css-1dbjc4n r-xoduu5 r-1udh08x'})
        print(
            f'Comments: {tweet_numbers[0].get_text()}, Retweets: {tweet_numbers[1].get_text()}, Likes: {tweet_numbers[2].get_text()}')
        print('Retweet: ', retweet_text.get_text())
        print()
        print()
    print(len(elements))
finally:
    # driver.quit()
    pass
