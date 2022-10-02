# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 8: Ngrams


import os
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle
import math


# Function to computure the probalities
def compute_prob(text, unigram_dict, bigram_dict, v):
    # v is the total vocabulary size (add the lengths of the 3 unigram dictionaries)

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    
    p_laplace = 1  # calculate p using Laplace smoothing
   
    for bigram in bigrams_test:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0             # b is the bigram count 
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0     # u is the unigram count of the first word in the bigram (From only current working language)

        p_laplace = p_laplace * ((b + 1) / (u + v))
       
    return p_laplace
    # print('probability with laplace smoothing is', p_laplace)

# main
def main():
    # Read pickle dictionaries and unpackage them
    # For English
    with open('english_uni_dict.pickle', 'rb') as handle:
        english_uni_dict = pickle.load(handle)
    with open('english_bi_dict.pickle', 'rb') as handle:
        english_bi_dict = pickle.load(handle)

    # For French
    with open('french_uni_dict.pickle', 'rb') as handle:
        french_uni_dict = pickle.load(handle)
    with open('french_bi_dict.pickle', 'rb') as handle:
        french_bi_dict = pickle.load(handle)

    # For Italian
    with open('italian_uni_dict.pickle', 'rb') as handle:
        italian_uni_dict = pickle.load(handle)
    with open('italian_bi_dict.pickle', 'rb') as handle:
        italian_bi_dict = pickle.load(handle)

    print(list(english_uni_dict.items())[:4])  # debug

    # V is the total vocabulary size (add the lengths of the 3 unigram dictionaries)
    v = len(english_uni_dict) + len(french_uni_dict) + len(italian_uni_dict)

# Debug
    # test_text = "Signora Presidente , vorrei sapere perché questo Parlamento non rispetta le norme in materia di salute e sicurezza che esso stesso approva ."
    test_text = "Is there a member who wishes to speak on behalf of this Group to propose this ?"
    # test_text = "C ' est en effet tout à fait dans la ligne des positions que notre Parlement a toujours adoptées ."
# Debug

    probab = []

    english_probab  = compute_prob(test_text, english_uni_dict, english_bi_dict, v)
    probab.append(english_probab)

    french_probab   = compute_prob(test_text, french_uni_dict, french_bi_dict, v)
    probab.append(french_probab)

    italian_probab  = compute_prob(test_text, italian_uni_dict, italian_bi_dict, v)
    probab.append(italian_probab)

    
    max_probab = max(probab)

    if english_probab == max_probab:
        print('Text is in English')

    if french_probab == max_probab:
        print('Text is in French')

    if italian_probab == max_probab:
        print('Text is in Italian')



if __name__ == "__main__":
    main()
