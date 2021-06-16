import requests
from bs4 import BeautifulSoup
url = 'https://twitter.com/search?q=%23BlackLivesMatter&src=typeahead_click&lang=en'

source = requests.get(url )
soup = BeautifulSoup(source.text, 'lxml')

print(soup.prettify())
