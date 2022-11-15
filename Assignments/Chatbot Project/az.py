import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from subprocess import call
import os
from nltk.corpus import stopwords
from collections import Counter
from nltk import sent_tokenize
from nltk import word_tokenize
from collections import Counter


str = 'who is william gibson?'

tokens = word_tokenize(str)
with open("stopwords.txt", 'r', encoding='utf-8') as f:
    stop_words = f.read()

stpwrd = stopwords.words('english')
stpwrd.extend(word_tokenize(stop_words))


ztokens = [t.lower() for t in tokens if t.isalpha() and t not in stpwrd]

print('ztoken', ztokens)