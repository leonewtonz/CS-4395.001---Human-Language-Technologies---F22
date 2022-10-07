# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 12: Web Crawler


# import os
# import nltk
# from nltk.util import ngrams
# import pickle
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
from nltk import sent_tokenize
from nltk import word_tokenize


## Web Crawler Function
def web_crawling(starter_url):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    # soup = BeautifulSoup(data)

    key_words = ['matrix', 'Matrix']

    # write urls to a file
    counter = 0
    with open('urls.txt', 'w') as f:
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            # print(link_str)
            if 'matrix' in link_str or 'Matrix' in link_str:
            # if 'matrix' in link_str:
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]
                if link_str.startswith('http') and 'google' not in link_str and 'bbfc' not in link_str:
                    if counter == 15: #  Get 15 relevant urls.
                        break
                    f.write(link_str + '\n')             
                    counter += 1

    print('15 urls saved to urls.txt')
    print("\n________End of web_crawling________")

## Function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

## Wed Scraper Function
def web_scraping(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, features='lxml')
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)      # list from filter

    # print(temp_list)  # debug. There a lot of \n

    temp_str = ' '.join(temp_list)  # Will content a lot of white space because of \n

    # print(temp_str)  # debug

    # Remove all white space. It is the same as remove the newline charactors
    text_chunks = [chunk for chunk in temp_str.splitlines() if not re.match(r'^\s*$', chunk)]
    # for i, chunk in enumerate(text_chunks):
    #     print(i+1, chunk)

    temp_str = ' '.join(text_chunks)  # Now we have decent clean text
    # print(temp_str)  # debug

    return temp_str

    print("\n________End of web_scraping________")

## Preprocessing Function
def preprocessing(text, file_order):
    sents = sent_tokenize(text)

# debug
    i = 1
    for sent in sents:
        print(i, ':', sent)
        i+=1
        tokens = [t.lower() for t in word_tokenize(sent) if t.isalpha()]
        print(tokens)
# debug
    file_name = str(file_order) + '.txt'
    with open(file_name, 'w') as f:
        for sent in sents:
            f.write(sent + '\n')     

## 25 Important Terms Function

## Chatbot-Searchable Knowledge Base Function
## main
def main():
    starter_url = "https://en.wikipedia.org/wiki/The_Matrix"
    
    # Web Crawler
    web_crawling(starter_url)

# # Debug
#     i = 1
#     with open('urls.txt', 'r') as f:
#         urls = f.read().splitlines()
#     for u in urls:
#         print(i, ':', u)
#         i += 1
# # Debug

    # Web Scraper
    url = 'https://www.vulture.com/2021/12/the-matrix-laid-the-template-for-the-modern-blockbuster.html'
    text_page = web_scraping(url)

    # Preprocessing
    preprocessing(text_page, 1)

    # 25 Important Term

    # Chatbot-Searchable Knowledge Base
        

    print('\n________End of main________')
if __name__ == "__main__":
    main()
