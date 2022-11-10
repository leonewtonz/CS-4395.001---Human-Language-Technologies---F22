# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002

# Porfolio: Chatbot Project

# This file was built based on web_scrawler.py from previous assignment

from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import pickle
from collections import Counter

NUM_URL = 15
NUM_IMPORTANT_TERM = 25


## Web Crawler Function
def web_crawling(starter_url, keyword):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # keyword = ['reviews', 'articles', 'cyberpunk']
    keyword = ['pet']
    # Extract 15 relevant urls
    counter = 0
    urls = []
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        for item in keyword:
            if item in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]

                if counter == 0:
                    if link_str.startswith('http') and 'google' not in link_str:
                        if counter == NUM_URL:  #
                            break
                        # print(link_str) # debug
                        try:
                            html = urllib.request.urlopen(link_str)
                            status_code = html.getcode()
                            # print(status_code) # debug
                            if status_code == 200:
                                urls.append(link_str)
                                counter += 1
                        except urllib.error.HTTPError:
                            pass
                        except urllib.error.URLError:
                            pass
                else:
                    dup_link = str(urls[counter - 1])
                    if link_str.startswith('http') and 'google' not in link_str and dup_link not in link_str:
                        if counter == NUM_URL:  #
                            break
                        # print(link_str) # debug
                        try:
                            html = urllib.request.urlopen(link_str)
                            status_code = html.getcode()
                            # print(status_code) # debug
                            if status_code == 200:
                                urls.append(link_str)
                                counter += 1
                        except urllib.error.HTTPError:
                            pass
                        except urllib.error.URLError:
                            pass

    return urls


## Wed Scraper Function
def web_scraping(urls):
    i = 0
    raw_data = ''
    while i < NUM_URL:

        # print('\n@@@', urls[i])  # debug

        html = urllib.request.urlopen(urls[i])
        soup = BeautifulSoup(html, features="xml")
        temp_list = []
        for p in soup.select('p'):
            # print(p.getText()) # debug
            temp_list.append(p.getText())

            temp_str = ' '.join(temp_list)

        page_name = 'p' + str(i + 1) + '.txt'
        with open(page_name, 'w', encoding='utf-8') as f:
            f.write(temp_str)

        raw_data = raw_data + temp_str
        i += 1

    # with open('raw_data.txt', 'w', encoding='utf-8') as f:
    #     f.write(raw_data)
    return raw_data.lower()


## Preprocessing Function
def preprocessing(raw_text):
    text_chunks = [chunk for chunk in raw_text.splitlines() if not re.match(r'^\s*$', chunk)]
    text = ' '.join(text_chunks)

    with open('corpus.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    sents_respond = sent_tokenize(text)
    pickle.dump(sents_respond, open('k_base.p', 'wb'))

## Function to find import term
def find_important_term(all_tokens):
    tokens = [t for t in all_tokens if t.isalpha() and t not in stopwords.words('english')]

    wordCounter = Counter(tokens)
    top25_words = wordCounter.most_common(NUM_IMPORTANT_TERM)

    print('\n\nTop 25 important words:\n', top25_words)

    return top25_words


## Chatbot-Searchable Knowledge Base Function
def build_knowledge_base(top10):
    know_base = {}
    list_words = []
    for a_tuple in top10:
        list_words.append(a_tuple[0])

    for i in list_words:
        req = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{i}")
        know_base[str(i)] = req.text

    print('\n\n Knowlege Base:\n', know_base)
    pickle.dump(know_base, open('k_base.p', 'wb'))


## main
def main():
    starter_url = "https://www.neondystopia.com/"

    # Web Crawler
    urls = web_crawling(starter_url)
    print('List of 15 relevants urls:')
    for url in urls:
        print(url)

    # Web Scraper
    # raw_text = web_scraping(urls)

    # Preprocessing
    # preprocessing(raw_text)

    # # Top 25 Important Terms
    # find_important_term(all_tokens)

    print('\n________Program End________')


if __name__ == "__main__":
    main()
