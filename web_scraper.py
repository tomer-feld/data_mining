from time import sleep
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

NUM = 50
CHROME_TWEET_CLASSES = {
    'time_of_tweet': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    'tweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0',
    'user_handle': 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'tweet_numbers': 'css-1dbjc4n r-xoduu5 r-1udh08x',
    'retweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0',
    'timeline': 'css-1dbjc4n'
}
# TODO: pick which languages we want to support
SUPPORTED_LANGUAGES = ['en', 'it', 'und', 'es', 'fr']


class Tweet:
    # TODO: right now init gets keyword parameters or dictionary of the properties,
    #  and we save them all as is. Need to change to have properties that always exist
    #  and others that don't (quote, comments)
    def __init__(self, **properties):
        self._properties = properties


def scrape_hashtag(num, hashtag, top_or_live='live', driver=webdriver.Chrome()):
    url = f"https://twitter.com/search?q=%23{hashtag}&lang=en&f={top_or_live}"
    try:
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        soups = set()
        # saving the elements into the soups set because once we scroll down we lose the elements

        elements = []
        height = {'y':0}
        while len(soups) < num:
            # get last element and its location and scroll ti its location
            if len(elements) > 0:
                height = elements[-1].location
            driver.execute_script(f"window.scrollTo(0,{height['y']})")
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, f"//div[@data-testid='tweet']")))
            # scrape all elements that driver can find after loading
            elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
            for element in elements:
                print([el.get_property('lang') for el in element.find_elements_by_xpath('//div[@lang]')])
                if all(el.get_property('lang') in SUPPORTED_LANGUAGES for el in
                       element.find_elements_by_xpath('//div[@lang]')):
                    soups.add(BeautifulSoup(element.get_attribute('innerHTML'), 'lxml'))

            print(len(soups))  # TODO: used for sanity checks, you can delete this after you've passed them
    finally:
        driver.quit()
    return soups


def extract_tweet_data(tweets, chrome_or_firefox='chrome'):
    # TODO: change this to create tweet class and input the relevant information into the tweet obj right now only prints
    # TODO: need to also allow firefox class names or better way to get tweet data
    for tweet in tweets:
        time_of_tweet = tweet.find('a', attrs={
            'class': CHROME_TWEET_CLASSES['time_of_tweet']})
        print(time_of_tweet.time['datetime'])

        tweet_text = tweet.find('div', attrs={'class': CHROME_TWEET_CLASSES['tweet_text']})

        user_handle = tweet.findAll('div', attrs={'class': CHROME_TWEET_CLASSES['user_handle']})
        print(f'Tweet by {user_handle[0].get_text()}: ', tweet_text.get_text())

        tweet_numbers = tweet.findAll('div', attrs={'class': CHROME_TWEET_CLASSES['tweet_numbers']})
        print(
            f'Comments: {tweet_numbers[0].get_text()}, Retweets: {tweet_numbers[1].get_text()}, Likes: {tweet_numbers[2].get_text()}')

        if tweet.find(text='Quote Tweet'):
            retweet_text = tweet.find('div', attrs={
                'class': CHROME_TWEET_CLASSES['retweet_text']})
            print(f'Retweet of {user_handle[1].get_text()}: ', retweet_text.get_text())
        print()
        print()
    print(len(tweets))


def main():
    raw_tweets = scrape_hashtag(NUM, 'BlackLivesMatter')
    extract_tweet_data(raw_tweets)


if __name__ == '__main__':
    main()
