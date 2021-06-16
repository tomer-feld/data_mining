import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# # set a global constant variable
# GET_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
# # and than when using requests in the function:
# # page = requests.get(url, headers=GET_HEADERS)
# # url = 'https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en'
# url = 'https://www.rottentomatoes.com/tv/the_umbrella_academy/s01'
# source = requests.get(url)
# soup = BeautifulSoup(source.text, 'html.parser')
# # tweets = soup.find_all("li", {"data-item-type": "tweet"})
# print(soup.prettify())
# print('########################## tweets ############################')
# # for tweet in tweets:
# #     print(tweet.prettify())
# PATH = '/usr/local/bin/geckodriver'
driver = webdriver.Firefox()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en"

driver.get(url)
print(driver)
driver.close()