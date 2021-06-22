from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

NUM = 30
CHROME_TWEET_CLASSES = {
    # 'time_of_tweet': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    # 'tweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0',
    'user_handle': 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'tweet_numbers': 'css-1dbjc4n r-xoduu5 r-1udh08x',
    'quoted_tweet': 'css-1dbjc4n r-1bs4hfb r-1867qdf r-rs99b7 r-1loqt21 r-adacv r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg',
    'retweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0',
    'timeline': 'css-1dbjc4n',
    'tags': 'css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1n1174f r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0'
}
FIREFOX_TWEET_CLASSES = {
    'time_of_tweet': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    'tweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0',
    'user_handle': 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'tweet_numbers': 'css-1dbjc4n r-xoduu5 r-1udh08x',
    'retweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0',
    'timeline': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    'tags': 'css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1n1174f r-1loqt21 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0'
}
# TODO: pick which languages we want to support
SUPPORTED_LANGUAGES = ['en', 'it', 'und', 'es', 'fr']
MIN_WAIT = 3
LIVE_OR_TOP = {'live': '&f=live', 'top': ''}


class Tweet:
    """

    """

    # TODO: Added mandatory properties still need to add optional arguments like quoted tweets. We might want to add
    #  links to comments or links to the tweet itself so we can use that data later or links to videos or images
    def __init__(self, user_handle, time_of_tweet, tweet_text, tags, stats=None, **properties):
        self._user_handle = user_handle
        self._time = time_of_tweet
        self._text = tweet_text
        self._stats = stats
        # TODO: In quoted tweets we don't have this info so we give it empty values even though this might now be true
        if not self._stats or self._stats is None:
            self._stats = [BeautifulSoup('<a></a>', 'lxml') for i in range(3)]
        self._tags = tags
        if self._tags is None:
            self._tags = []
        self._properties = properties

    def get_time(self):
        """returns the datetime stamp of the tweet in ISO format"""
        return self._time

    def get_text(self):
        """ returns tha plain text of the tweet"""
        return self._text.get_text()

    def get_user_handle(self):
        """returns the user handle of the tweet poster"""
        return self._user_handle[0].get_text()

    def get_stats(self):
        """returns the number of comments, retweets and likes"""
        return [stat.get_text() if stat.get_text() != '' else '0' for stat in self._stats]

    def get_properties(self):
        return self._properties

    def get_hashtags(self):
        """returns a list of all the hashtags used in the tweet"""
        return [tag.get_text() for tag in self._tags if tag.get_text().startswith('#')]

    def get_mentions(self):
        """returns a list of al the users mentioned in the tweet"""
        return [tag.get_text() for tag in self._tags if tag.get_text().startswith('@')]

    def __str__(self):
        """displays the content of the tweet object"""
        quote = "" if self._properties["quoted_tweet"] is None \
            else "\nQuoted Tweet: \n\t" + str(self._properties["quoted_tweet"]).replace('\n', '\n\t') + \
                 "\nEnd Quoted Tweet"
        return f'{self.get_time()} \nTweet by {self.get_user_handle()}: {self.get_text()}\n' \
               f'Comments: {self.get_stats()[0]}, Retweets: {self.get_stats()[1]}, Likes: {self.get_stats()[2]}\n' \
               f'Mentions: {self.get_mentions()}\nHashtags: {self.get_hashtags()}' \
               f'{quote}'


def scrape_hashtag(num, hashtag, min_wait=MIN_WAIT, top_or_live='live', driver=webdriver.Chrome()):
    """
    Opens the desired twitter hashtag page and returns a set containing all the raw tweets html data.
    closes the page at the end
    :param num: int. Number of desired tweets for scraping
    :param hashtag: string. Hashtag for scraping
    :param top_or_live: string. choose if scraping the top or the live tweets. default is 'live'
    :param driver: the Selenium driver
    :return: Set of raw tweets
    """
    url = f"https://twitter.com/search?q=%23{hashtag}&lang=en{LIVE_OR_TOP[top_or_live]}"
    # saving the elements into the soups set because once we scroll down we lose the elements
    soups = set()
    try:
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, min_wait)
        height = 0
        # last_height = height
        with tqdm(total=NUM) as pbar:
            while len(soups) < num:
                # get last element and its location and scroll to its location
                driver.execute_script(f"window.scrollTo(0,{height})")
                wait.until(EC.visibility_of_all_elements_located((By.XPATH, f"//div[@data-testid='tweet']")))
                # scrape all elements that driver can find after loading
                elements = driver.find_elements_by_xpath(r"//div[@data-testid='tweet']")
                if len(elements) > 0:
                    height = elements[-1].location['y']
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
    """
    Creates a list of tweet objects of class Tweet from a set of raw html tweet elements.
    :param tweets: iterable containing html tweet elements
    :param chrome_or_firefox: specify from which browser the data was scraped. Relevant for class names
    :return: a list of tweet objects
    """
    # TODO: need to also allow firefox class names or better way to get tweet data
    extracted_tweets = []
    if chrome_or_firefox == 'chrome':
        class_dict = CHROME_TWEET_CLASSES
    else:
        class_dict = FIREFOX_TWEET_CLASSES
    for tweet in tweets:
        time_of_tweet = tweet.find('time')['datetime']
        tweet_text = tweet.find('div', attrs={'lang': SUPPORTED_LANGUAGES})
        user_handle = tweet.findAll('div', attrs={'class': class_dict['user_handle']})
        tweet_numbers = tweet.findAll('div', attrs={'class': class_dict['tweet_numbers']})
        quoted_tweet_data = tweet.find('div', attrs={'class': class_dict['quoted_tweet']})
        quoted_tweet = None
        if quoted_tweet_data is not None:
            quoted_tweet = extract_tweet_data([quoted_tweet_data], chrome_or_firefox)[0]
        extracted_tweets.append(
            Tweet(user_handle, time_of_tweet, tweet_text, stats=tweet_numbers, quoted_tweet=quoted_tweet))
    return extracted_tweets


def present_tweets(tweets):
    """
    Present tweets to the console
    :param tweets: lists of tweets
    :return:
    """
    for tweet in tweets:
        print(tweet, '\n\n')


def save_to_csv(tweets, file_name, overwrite=False):
    """
    saves the data to a csv file
    :param tweets: list of tweet objects
    :param file_name: path to file
    :param overwrite: choose whether to allow overwriting of existing file. Default=False
    :return:
    """
    if os.path.isfile(file_name) and not overwrite:
        print("File already exist. Didn't overwrite")
        return
    df = pd.DataFrame(columns=('user_handle', 'time_stamp', 'text', 'stats', 'mentions', 'hashtags'))
    for tweet in tweets:
        data = [tweet.get_user_handle(), tweet.get_time(), tweet.get_text(),
                tweet.get_stats(), tweet.get_mentions(), tweet.get_hashtags()]
        row = pd.Series(data, index=df.columns)
        df = df.append(row, ignore_index=True)
    df.to_csv(file_name)


# TODO: need to create function that exports tweets to file, and maybe also importer
def main():
    raw_tweets = scrape_hashtag(NUM, 'BlackLivesMatter', MIN_WAIT, 'live')
    tweets = extract_tweet_data(raw_tweets)
    present_tweets(tweets)
    save_to_csv(tweets, 'test.csv',overwrite=True)


if __name__ == '__main__':
    main()
