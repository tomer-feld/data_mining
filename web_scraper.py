from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import argparse
import pandas as pd

NUM = 30
CHROME_TWEET_CLASSES = {
    # 'time_of_tweet': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    # 'tweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0',
    # 'user_handle': 'css-901oao css-bfa6kz r-m0bqgq r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'user_handle': 'css-901oao css-bfa6kz r-14j79pv r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'tweet_numbers': 'css-1dbjc4n r-xoduu5 r-1udh08x',
    # 'quoted_tweet': 'css-1dbjc4n r-1bs4hfb r-1867qdf r-rs99b7 r-1loqt21 r-adacv r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg',
    # 'retweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0',
    # 'timeline': 'css-1dbjc4n',
    'tags': 'css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1n1174f r-1loqt21 r-poiln3 r-bcqeeo r-qvutc0'
}
FIREFOX_TWEET_CLASSES = {
    # 'time_of_tweet': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    # 'tweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0',
    'user_handle': 'css-901oao css-bfa6kz r-9ilb82 r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0',
    'tweet_numbers': 'css-1dbjc4n r-xoduu5 r-1udh08x',
    # 'quoted_tweet': 'css-1dbjc4n r-1bs4hfb r-1867qdf r-rs99b7 r-1loqt21 r-adacv r-1ny4l3l r-1udh08x r-o7ynqc r-6416eg',
    # 'retweet_text': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-14gqq1x r-bcqeeo r-bnwqim r-qvutc0',
    # 'timeline': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0',
    'tags': 'css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1n1174f r-1loqt21 r-poiln3 r-b88u0q r-bcqeeo r-qvutc0'
}
# TODO: pick which languages we want to support
SUPPORTED_LANGUAGES = ['en', 'it', 'und', 'es', 'fr']
MAX_WAIT = 3
LIVE_OR_TOP = {'live': '&f=live', 'top': ''}


class Tweet:
    """
    Class object for tweets
    """

    def __init__(self, user_handle, time_of_tweet, tweet_text, tags, stats=None, quoted_tweet=None, **properties):
        self._user_handle = user_handle
        self._time = time_of_tweet
        self._text = tweet_text
        self._stats = stats
        if not self._stats or self._stats is None:
            self._stats = ['', '', '']
        self._tags = tags
        if self._tags is None:
            self._tags = []
        self._quoted_tweet = quoted_tweet
        self._properties = properties

    def get_time(self):
        """returns the datetime stamp of the tweet in ISO format"""
        return self._time

    def get_text(self):
        """ returns tha plain text of the tweet"""
        return self._text

    def get_user_handle(self):
        """returns the user handle of the tweet poster"""
        return self._user_handle

    def get_stats(self):
        """returns the number of comments, retweets and likes"""
        return [stat if stat != '' else '0' for stat in self._stats]

    def get_properties(self):
        """
        :return: a dictionary
        """
        return self._properties

    def get_hashtags(self):
        """returns a list of all the hashtags used in the tweet"""
        return [tag.get_text() for tag in self._tags if tag.get_text().startswith('#')]

    def get_mentions(self):
        """returns a list of al the users mentioned in the tweet"""
        return [tag.get_text() for tag in self._tags if tag.get_text().startswith('@')]

    def get_quoted_tweet(self):
        """
        :return: a Tweet object
        """
        return self._quoted_tweet

    def __repr__(self):
        """
        :return: representation of the tweet
        """
        d_of_tweet = {'text': self._text, 'user_handle': self._user_handle, 'time': self._time,
                      'tags': self._tags, 'stats': self._stats, 'quoted_tweet': self._quoted_tweet,
                      'properties': self._properties}
        return str(d_of_tweet)

    def __str__(self):
        """displays the content of the tweet object"""
        quote = "" if self.get_quoted_tweet() is None \
            else "\nQuoted Tweet: \n\t" + str(self.get_quoted_tweet()).replace('\n', '\n\t') + \
                 "\nEnd Quoted Tweet"
        return f'{self.get_time()} \nTweet by {self.get_user_handle()}: {self.get_text()}\n' \
               f'Comments: {self.get_stats()[0]}, Retweets: {self.get_stats()[1]}, Likes: {self.get_stats()[2]}\n' \
               f'Mentions: {self.get_mentions()}\nHashtags: {self.get_hashtags()}' \
               f'{quote}'


def open_driver(chrome_or_firefox):
    """
    creates webpage of either type
    :param chrome_or_firefox:
    :return: driver object
    """
    if chrome_or_firefox == 'chrome':
        return webdriver.Chrome()
    elif chrome_or_firefox == 'firefox':
        return webdriver.Firefox()


def scrape_hashtag(hashtag, num=NUM, max_wait=MAX_WAIT, top_or_live='live', chrome_or_firefox='chrome'):
    """
    Opens the desired twitter hashtag page and returns a set containing all the raw tweets html data.
    closes the page at the end
    :param chrome_or_firefox: string denoting which webdriver to use
    :param max_wait: maximum wait time for elements to load
    :param num: int. Number of desired tweets for scraping
    :param hashtag: string. Hashtag for scraping
    :param top_or_live: string. choose if scraping the top or the live tweets. default is 'live'
    :return: Set of raw tweets
    """
    url = f"https://twitter.com/search?q=%23{hashtag}&lang=en{LIVE_OR_TOP[top_or_live]}"
    # saving the elements into the soups set because once we scroll down we lose the elements
    soups = set()
    with open_driver(chrome_or_firefox) as driver:
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, max_wait)
        height = 0
        # last_height = height
        with tqdm(total=num) as pbar:
            while len(soups) < num:
                # get last element and its location and scroll to its location
                driver.execute_script(f"window.scrollTo(0,{height})")
                wait.until(ec.visibility_of_all_elements_located((By.XPATH, f"//div[@data-testid='tweet']")))
                wait.until(ec.visibility_of_all_elements_located((By.XPATH, f"//div[@lang]")))
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
    return soups


def extract_tweet_data(tweets, chrome_or_firefox='chrome'):
    """
    Creates a list of tweet objects of class Tweet from a set of raw html tweet elements.
    :param tweets: iterable containing html tweet elements
    :param chrome_or_firefox: specify from which browser the data was scraped. Relevant for class names
    :return: a list of tweet objects
    """
    extracted_tweets = []
    if chrome_or_firefox == 'chrome':
        class_dict = CHROME_TWEET_CLASSES
    else:
        class_dict = FIREFOX_TWEET_CLASSES
    for tweet in tweets:
        time_of_tweet = tweet.find('time')['datetime']
        tweet_text = tweet.find('div', attrs={'lang': SUPPORTED_LANGUAGES})
        tags = tweet_text.findAll('a', attrs={'class': class_dict['tags']})
        tweet_text = tweet_text.get_text()
        user_handle = tweet.find('div', attrs={'class': class_dict['user_handle']}).get_text()
        tweet_numbers = [stat.get_text() for stat in tweet.findAll('div', attrs={'class': class_dict['tweet_numbers']})]
        quoted_tweet_data = tweet.find('div', attrs={'role': 'link'})
        quoted_tweet = None
        if quoted_tweet_data is not None:
            quoted_tweet = extract_tweet_data([quoted_tweet_data], chrome_or_firefox)[0]
        extracted_tweets.append(
            Tweet(user_handle, time_of_tweet, tweet_text, tags, stats=tweet_numbers, quoted_tweet=quoted_tweet))
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
    df = pd.DataFrame(columns=('user_handle', 'time_stamp', 'text', 'stats', 'tags', 'quoted_tweet'))
    for tweet in tweets:
        data = [tweet.get_user_handle(), tweet.get_time(), tweet.get_time(),
                tweet.get_stats(), tweet._tags, repr(tweet.get_quoted_tweet())]
        row = pd.Series(data, index=df.columns)
        df = df.append(row, ignore_index=True)
    df.to_csv(file_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='any hashtag for twitter')
    parser.add_argument('-min_tweets', help='minimum amount of tweets to scrap', type=int,
                        default=NUM)
    parser.add_argument('-c_f', metavar='chrome_or_firefox', help='Browser to use', choices=['chrome', 'firefox'],
                        default='chrome')
    parser.add_argument('-t_l', metavar='top_or_live', help='Get the live tweets or top tweets of hashtag',
                        choices=['top', 'live'], default='live')
    parser.add_argument('-file', help='File to write to', default='tweets.csv')
    parser.add_argument('-max_wait', help='Maximum wait time', default=MAX_WAIT)
    parser.add_argument('-p', help='print out tweets to console', action='store_true')
    args = parser.parse_args()
    if not os.path.exists(os.path.dirname(os.path.abspath(args.file))) or not args.file.endswith('.csv'):
        print('Can only create csv files.')
        exit(1)
    if args.t_l == 'top' and args.min_tweets > 50:
        print('Need to implement exit out of loop when reached last tweet.\nFor now limited top to 50')
        exit(1)
    if args.max_wait < MAX_WAIT:
        print('Not allowing you to get errors to reduce the wait time.')
        exit(1)
    raw_tweets = scrape_hashtag(args.hashtag, args.min_tweets, max_wait=args.max_wait, chrome_or_firefox=args.c_f,
                                top_or_live=args.t_l)
    tweets = extract_tweet_data(raw_tweets, chrome_or_firefox=args.c_f)
    if args.p:
        present_tweets(tweets)
    save_to_csv(tweets, args.file, overwrite=True)


if __name__ == '__main__':
    main()
