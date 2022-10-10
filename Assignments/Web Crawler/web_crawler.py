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
import math
import pickle
import wordhoard
import socket



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
                if counter == 15: #  
                    break
                print(link_str)
                try:
                    html = urllib.request.urlopen(link_str)
                    status_code = html.getcode()
                    print(status_code) # debug
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
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

## Wed Scraper Function
def web_scraping(url, page_index):

    
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, features="lxml")
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)      # list from filter
    temp_str = ' '.join(temp_list)
    # print(repr(temp_str)) # debug

    page_name = 'p' + str(page_index) + '.txt'
    with open(page_name, 'w', encoding='utf-8') as f:
        f.write(temp_str)

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
   

## tf_dict funct
def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc)
    tokens = [w for w in tokens if w.isalpha() and w not in stopwords.words('english')]
     
    # Get term frequency
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) for t in token_set}
    
    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
        
    return tf_dict

## tfidf function
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t] 
        
    return tf_idf

## 25 Important Terms Function
def find_25terms():
    vocab = set()
    list_tf_dicts = []
    list_tfidf = []

    index = 1
    while(index < 16):
        path = str(index) + '.txt'
        with open(path, 'r', encoding='utf-8') as f:
            doc = f.read().lower()
            doc = doc.replace('\n', ' ')
            list_tf_dicts.append(create_tf_dict(doc))
            index += 1

    for tf in list_tf_dicts:
        vocab = vocab.union(set(tf.keys()))

    print('Number of unique words:', len(vocab))

    idf_dict = {}
    num_docs = len(list_tf_dicts)
    vocab_by_topic = [tf.keys() for tf in list_tf_dicts]
    for term in vocab:
        temp = ['x' for voc in vocab_by_topic if term in voc]
        idf_dict[term] = math.log((1+num_docs) / (1+len(temp))) 

    for dict in list_tf_dicts:
        list_tfidf.append(create_tfidf(dict, idf_dict))

    combine_tfidf = {}
    for d in list_tfidf:
        doc_term_weights = sorted(d.items(), key=lambda x:x[1], reverse=True)
        # print("\n@@@", doc_term_weights[:5])  # debug
        combine_tfidf = combine_tfidf | d

    top25 = []
    doc_term_weights = sorted(combine_tfidf.items(), key=lambda x:x[1], reverse=True)
    print("\n@@@", doc_term_weights[:30])


    for tuple in doc_term_weights[:25]:
        top25.append(tuple)

    return top25

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
    page_index = 1
    for url in urls:
        web_scraping(url, page_index)
        page_index += 1

  
    # Preprocessing
    index = 1
    while(index < 16):
        path = 'p' + str(index) + '.txt'
        with open(path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            preprocessing(raw_text, index)
            index += 1


    # 25 Important Term
    top25 = find_25terms()
    # print(top25)



    # # Chatbot-Searchable Knowledge Base
    # build_knowledge_base(top25)
        

    print('\n________End of main________')
if __name__ == "__main__":
    main()
