# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 8: Ngrams


import os
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
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


    # V is the total vocabulary size (add the lengths of the 3 unigram dictionaries)
    v = len(english_uni_dict) + len(french_uni_dict) + len(italian_uni_dict)

    # Calculate the language probability for each sentence in test file
    sents = list(open('ngram_files/LangId.test', 'r'))

    probab_result = open("output.txt", "w")  # This is the output file for calculated probabilities of each language     

    i = 1
    for sent in sents:
        probab = []

        english_probab  = compute_prob(sent, english_uni_dict, english_bi_dict, v)
        probab.append(english_probab)

        french_probab   = compute_prob(sent, french_uni_dict, french_bi_dict, v)
        probab.append(french_probab)

        italian_probab  = compute_prob(sent, italian_uni_dict, italian_bi_dict, v)
        probab.append(italian_probab)

        max_probab = max(probab)

        # Write the highest probability to file
        if english_probab == max_probab:
            probab_result.write(str(i) + ' English\n')
            i += 1
        elif french_probab == max_probab:
            probab_result.write(str(i) + ' French\n') 
            i += 1
        elif italian_probab == max_probab:
            probab_result.write(str(i) + ' Italian\n') 
            i += 1

    probab_result.close()

    # Compute the accuracy
    output      = list(open("output.txt", "r"))
    solution    = list(open('ngram_files/LangId.sol', 'r'))

    num_correct = 0
    incorrect_lines = []
    for i in range(len(output)):
        if output[i] == solution[i]:
            num_correct += 1
        else:
            incorrect_lines.append(output[i].replace("\n", ""))

    accuracy = (num_correct/len(solution))*100

    print('Accuracy: %.2f percent' % accuracy)
    print('List of incorrectly classified items:')
    for item in incorrect_lines:
        print(item)

if __name__ == "__main__":
    main()
