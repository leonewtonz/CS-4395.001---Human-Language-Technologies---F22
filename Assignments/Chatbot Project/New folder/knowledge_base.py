# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002
#         Amol Perubhatla - AVP180003

# Porfolio: Chatbot Project
import nltk
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import pickle
from collections import Counter

NUM_URL = 10
NUM_IMPORTANT_TERM = 25


## Web Crawler Function
def web_crawling(starter_url, checked_urls):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # Extract 10 urls
    counter = 0
    urls = []
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'cyberpunk' in link_str or 'Cyberpunk' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]

            if counter == 0 and link_str not in checked_urls:
                if link_str.startswith('http') \
                                        and 'google' not in link_str \
                                        and '#comments' not in link_str \
                                        and '#respond' not in link_str \
                                        and '.pdf' not in link_str:
                    if counter == NUM_URL:
                        break
                    # print(link_str) # debug
                    try:
                        html = urllib.request.urlopen(link_str)
                        status_code = html.getcode()
                        # print(status_code) # debug
                        if status_code == 200:
                            urls.append(link_str)
                            checked_urls.append(link_str)
                            counter += 1
                    except urllib.error.HTTPError:
                        pass
                    except urllib.error.URLError:
                        pass
            else:
                if link_str not in checked_urls:
                    if link_str.startswith(
                            'http') and 'google' not in link_str and '#comments' not in link_str and '#respond' not in link_str:
                        if counter == NUM_URL:  #
                            break
                        # print(link_str) # debug
                        try:
                            html = urllib.request.urlopen(link_str)
                            status_code = html.getcode()
                            # print(status_code) # debug
                            if status_code == 200:
                                urls.append(link_str)
                                checked_urls.append(link_str)
                                counter += 1
                        except urllib.error.HTTPError:
                            pass
                        except urllib.error.URLError:
                            pass
    return urls


## Wed Scraper Function
def web_scraping(urls, checked_urls):
    k_base = []
    for url in urls:
        topic_urls = web_crawling(url, checked_urls)

        i = 0
        raw_text = ''
        temp_str = ''

        while i < len(topic_urls):
            html = urllib.request.urlopen(topic_urls[i])
            soup = BeautifulSoup(html, features="xml")
            temp_list = []
            for p in soup.select('p'):
                # print(p.getText()) # debug
                temp_list.append(p.getText())

                temp_str = ' '.join(temp_list)

            raw_text = raw_text + temp_str
            i += 1
        # print('\n@@@@\n', raw_text)
        sents = preprocessing(raw_text)

        k_base.extend(sents)

    pickle.dump(k_base, open('k_base.p', 'wb'))

# Preprocessing Function
def preprocessing(raw_text):
    text_chunks = [chunk for chunk in raw_text.splitlines() if not re.match(r'^\s*$', chunk)]
    text = ' '.join(text_chunks)

    sents = sent_tokenize(text)

    return sents

## main
def main():
    starter_url = "https://www.neondystopia.com/"

    # Web Crawler
    checked_urls = []
    urls = web_crawling(starter_url, checked_urls)
    print('Top 10 relevant topic:')
    print(*urls, sep = '\n')

    # Web Scraper
    web_scraping(urls, checked_urls)

if __name__ == "__main__":
    main()
