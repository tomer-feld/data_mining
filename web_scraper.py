from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en&f=live"
NUM = 1000
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
        time_of_tweet = soup.find('a', attrs={
            'class': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0'})
        # print(time_of_tweet)
        # tweet_url = re.findall('href=\S*status\S*',time_of_tweet)[0]
        # print(f'url: {tweet_url}')
        print(time_of_tweet.time)  # todo: parse with regexp

        tweet_text = soup.find('div', attrs={
            'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})

        user_handle = soup.findAll('div', attrs={
            'class': 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'})
        print(f'Tweet by {user_handle[0].get_text()}: ', tweet_text.get_text())

        tweet_numbers = soup.findAll('div', attrs={'class': 'css-1dbjc4n r-xoduu5 r-1udh08x'})
        print(
            f'Comments: {tweet_numbers[0].get_text()}, Retweets: {tweet_numbers[1].get_text()}, Likes: {tweet_numbers[2].get_text()}')

        if soup.find(text='Quote Tweet'):
            retweet_text = soup.find('div', attrs={
                'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0'})
            print(f'Retweet of {user_handle[1].get_text()}: ', retweet_text.get_text())
        print()
        print()
    print(len(soups))
finally:
    driver.quit()
    pass
