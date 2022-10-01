# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 5: Word Guess Game


import os
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import pickle


# Function to handle the filepath in both Window and Mac
def read_file(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        input_file = f.read()
    return input_file


# Function to create unigram dictionary and bigram dictionary
def dictionary(language):
    fp = 'ngram_files/' + language
    raw_text = read_file(fp)
    text = raw_text.replace('\n', ' ')  # remove newlines character
    tokens = word_tokenize(text)

    # print('\n\n', text[:50])  # debug
    # print('\n\n', tokens[:50]) # debug

    # Create unigrams list and unigrams dictionary
    unigrams = list(ngrams(tokens, 1))
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}

    # Create bigrams list and bigrams dictionary
    bigrams = list(ngrams(tokens, 2))
    bigram_dict = {t: bigrams.count(t) for t in set(bigrams)}

    return unigram_dict, bigram_dict

# # debug
#     print('\n\n', unigrams[:50])  # debug
#     count = 1
#     for uni in unigram_dict.keys():
#         print(uni, '->', unigram_dict[uni])
#         count += 1
#         if count > 5:
#             break
# # debug

# # debug
#     print('\n\n', bigrams[:50])  # debug
#     count = 1
#     for bi in bigram_dict.keys():
#         print(bi, '->', bigram_dict[bi])
#         count += 1
#         if count > 5:
#             break
# # debug


# main
def main():

    # Create unigrams and bigrams dictionary for English, French, Italian
    english_uni_dict, english_bi_dict = dictionary('LangId.train.English')
    french_uni_dict, french_bi_dict = dictionary('LangId.train.French')
    italian_uni_dict, italian_bi_dict = dictionary('LangId.train.Italian')

    # Pickle dictionary
    # For ENGLISH
    with open('english_uni_dict.pickle', 'wb') as handle:
        pickle.dump(english_uni_dict.pickle, handle)
    with open('english_bi_dict.pickle', 'wb') as handle:
        pickle.dump(english_bi_dict.pickle, handle)

    # For FRENCH
    with open('french_uni_dict.pickle', 'wb') as handle:
        pickle.dump(french_uni_dict.pickle, handle)
    with open('french_bi_dict.pickle', 'wb') as handle:
        pickle.dump(french_bi_dict.pickle, handle)

    # For ITALIAN
    with open('italian_uni_dict.pickle', 'wb') as handle:
        pickle.dump(italian_uni_dict.pickle, handle)
    with open('italian_bi_dict.pickle', 'wb') as handle:
        pickle.dump(italian_bi_dict.pickle, handle)


if __name__ == "__main__":
    main()
