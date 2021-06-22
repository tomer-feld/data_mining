# data_mining
Tomer Feld and Aaron Reuven,
We chose to work on scraping tweets from specific hashtags on twitter. We had difficulty accessing the elements in the
html file so we had to use Selenium and even still we had to manually find the names of different containers that
held the elements we wanted to scrape. We also used Selenium to scroll down the web page and load more tweets.
You can run the the code using the requirements.txt to install the specific modules we used and running the
web_scraper in the command line.
NOTE: you must have chromedriver or geckodriver executable (depending if you use chrome or firefox accordingly) in the PATH
and chrome or firefox installed
NOTE II: We've added the latest drivers to date in the project for windows users

usage: hashtag [-h] [-min_tweets MIN_TWEETS] [-c_f chrome_or_firefox] [-t_l top_or_live] 
[-file FILE] [-max_wait MAX_WAIT] [-p]

-h: help shows the help description

-min_tweets: amount of tweets to scrap 

-c_f: choose either browser to use (either chrome or firefox) default is chrome

-t_l: choose either to scrap the most popular tweets or the latest tweets of the hashtag default is latest

-file: where to save a csv file default is tweets.csv

-max_wait: choose maximum time to wait for elements to load default is 3 (this isn't that relevant because 
We're not allowing less than 3 seconds and 3 seconds should be enough)
                  
