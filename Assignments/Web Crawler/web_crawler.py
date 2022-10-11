# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002
#         Amol Perubhatla - AVP180003

# Porfolio Chapter 12: Web Crawler


from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import pickle
from collections import Counter



## Web Crawler Function
def web_crawling(starter_url):
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # Extract 15 relevant urls
    counter = 0
    urls = []
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'Reeves' in link_str or 'reeves' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                if counter == 1: #  
                    break
                # print(link_str) # debug
                try:
                    html = urllib.request.urlopen(link_str)
                    status_code = html.getcode()
                    # print(status_code) # debug
                    if(status_code == 200):
                        urls.append(link_str)
                        counter += 1    
                except urllib.error.HTTPError:
                    pass
                except urllib.error.URLError:
                    pass

                                
    return urls    

## Function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'nav']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

## Wed Scraper Function
def web_scraping(urls):

    i = 0
    while i < 1:
        # html = urllib.request.urlopen(urls[i])
        # soup = BeautifulSoup(html, features="lxml")
        # data = soup.findAll(text=True)
        # result = filter(visible, data)
        # temp_list = list(result)      # list from filter
        # temp_str = ' '.join(temp_list)
        # # print(repr(temp_str)) # debug

        # # temp_str =  str(i)
        # # soup = BeautifulSoup(html, features="lxml")
        # # for p in soup.select('p'):
        # #     soup1 = BeautifulSoup(p, features="lxml")
        # #     print (''.join(text.strip() for text in soup1.p.find_all(text=True, recursive=False)))
       
        html = urllib.request.urlopen(urls[i])
        soup = BeautifulSoup(html, features="lxml")
        temp_list = []
        for p in soup.select('p'):
            # print(p.getText()) # debug
            temp_list.append(p.getText())

        # print('\n@@@@@@@@@', temp_list)
        temp_str = ' '.join(temp_list)
        print(repr(temp_str))

        page_name = 'p' + str(i+1) + '.txt'
        with open(page_name, 'w', encoding='utf-8') as f:
            f.write(temp_str)

        i += 1

    # print("\n________End of web_scraping________")

## Preprocessing Function
def preprocessing(raw_text, index):

    text_chunks = [chunk for chunk in raw_text.splitlines() if not re.match(r'^\s*$', chunk)]
    text = ' '.join(text_chunks)

    sents = sent_tokenize(text)
    name_text = str(index) + '.txt'
    with open(name_text, 'w', encoding='utf-8') as f:
        for sent in sents:
            f.write(str(sent) + '\n\n')
   
## Function to find import term
def find_important_term():

    a
    index = 1
    while(index < 16):
        path = 'p' + str(index) + '.txt'
        with open(path, 'r', encoding='utf-8') as f:
            sents = f.read()
            index += 1

    tokens = word_tokenize(all_text)
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    wordCounter = Counter(tokens)
    top25_words = wordCounter.most_common(25)
    print(top25_words)

## Chatbot-Searchable Knowledge Base Function
def build_knowledge_base(top25):
    # tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    # wordCounter = Counter(tokens)
    # top_words = wordCounter.most_common(25)
    # print(top_words)
    know_base = {}
    list_words = []
    for a_tuple in top25:
        list_words.append(a_tuple[0])

    print(list_words)
    for i in list_words[:10]:
        req = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/%7Bi%7D%22")
        know_base[str(i)] = req.text

    print('\n\n', know_base)
    pickle.dump(know_base, open('k_base.p', 'wb'))



## main
def main():
    starter_url = "https://en.wikipedia.org/wiki/Keanu_Reeves"

    # Web Crawler
    urls = web_crawling(starter_url)
    print('List of 15 relevants urls:')
    for url in urls:
        print(url)

    # Web Scraper
    web_scraping(urls)
   
  
    # # Preprocessing
    # index = 1
    # while(index < 16):
    #     path = 'p' + str(index) + '.txt'
    #     with open(path, 'r', encoding='utf-8') as f:
    #         raw_text = f.read()
    #         preprocessing(raw_text, index)
    #         index += 1


    # # # Top 25 Important Terms
    # find_important_term()



    # # Chatbot-Searchable Knowledge Base
    # build_knowledge_base(top25)
        

    print('\n________End of main________')
if __name__ == "__main__":
    main()
