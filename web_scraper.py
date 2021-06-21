from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm

NUM = 200
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
    # TODO: Added mandatory properties still need to add optional arguments like quoted tweets. We might want to add
    #  links to comments or links to the tweet itself so we can use that data later or links to videos or images
    def __init__(self, user_handle, time_of_tweet, tweet_text, stats=None, **properties):
        self._user_handle = user_handle
        self._time = time_of_tweet
        self._text = tweet_text
        self._stats = stats  # TODO: What to do with this info
        if self._stats is None:
            self._stats = []
        self._properties = properties

    def get_time(self):
        return self._time.time['datetime']

    def get_text(self):
        return self._text.get_text()

    def get_user_handle(self):
        return self._user_handle[0].get_text()

    def get_stats(self):
        return [stat.get_text() if stat.get_text() != '' else '0' for stat in self._stats]

    def get_properties(self):
        return self._properties


def scrape_hashtag(num, hashtag, top_or_live='live', driver=webdriver.Chrome()):
    url = f"https://twitter.com/search?q=%23{hashtag}&lang=en&f={top_or_live}"
    try:
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        soups = set()
        # saving the elements into the soups set because once we scroll down we lose the elements
        elements = []
        height = {'y': 0}
        with tqdm(total=NUM) as pbar:
            while len(soups) < num:
                # get last element and its location and scroll to its location
                if len(elements) > 0:
                    height = elements[-1].location
                driver.execute_script(f"window.scrollTo(0,{height['y']})")
                wait.until(EC.visibility_of_all_elements_located((By.XPATH, f"//div[@data-testid='tweet']")))
                # scrape all elements that driver can find after loading
                elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
                for element in elements:
                    if all(el.get_property('lang') in SUPPORTED_LANGUAGES for el in
                           element.find_elements_by_xpath('//div[@lang]')):
                        old = len(soups)
                        soups.add(BeautifulSoup(element.get_attribute('innerHTML'), 'lxml'))
                        pbar.update(len(soups) - old)
    finally:
        driver.quit()
    return soups


def extract_tweet_data(tweets, chrome_or_firefox='chrome'):
    # TODO: need to also allow firefox class names or better way to get tweet data
    extracted_tweets = []
    for tweet in tweets:
        time_of_tweet = tweet.find('a', attrs={'class': CHROME_TWEET_CLASSES['time_of_tweet']})
        tweet_text = tweet.find('div', attrs={'class': CHROME_TWEET_CLASSES['tweet_text']})
        user_handle = tweet.findAll('div', attrs={'class': CHROME_TWEET_CLASSES['user_handle']})
        tweet_numbers = tweet.findAll('div', attrs={'class': CHROME_TWEET_CLASSES['tweet_numbers']})

        # TODO: still need to address the quoted tweet
        if tweet.find(text='Quote Tweet'):
            retweet_text = tweet.find('div', attrs={
                'class': CHROME_TWEET_CLASSES['retweet_text']})
            # print(f'Retweet of {user_handle[1].get_text()}: ', retweet_text.get_text())
        extracted_tweets.append(Tweet(user_handle, time_of_tweet, tweet_text, stats=tweet_numbers))
    return extracted_tweets


def present_tweets(tweets):
    """
    Present tweets to the console
    :param tweets: lists of tweets
    :return:
    """
    for tweet in tweets:
        print(tweet.get_time())
        print(f'Tweet by {tweet.get_user_handle()}: ', tweet.get_text())
        print(f'Comments: {tweet.get_stats()[0]}, Retweets: {tweet.get_stats()[1]}, Likes: {tweet.get_stats()[2]}')
        print()
        print()


def main():
    raw_tweets = scrape_hashtag(NUM, 'BlackLivesMatter')
    tweets = extract_tweet_data(raw_tweets)
    present_tweets(tweets)


if __name__ == '__main__':
    main()
