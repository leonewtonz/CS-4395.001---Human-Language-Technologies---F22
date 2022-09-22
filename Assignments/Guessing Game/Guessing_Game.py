# CS 4395.001 - NLP
# Leo Nguyen
# NetID: ldn190002

# Porfolio Chapter 5: Word Guess Game


import sys
import os
import nltk
import random

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


# Preprocessing raw text
def text_processing(raw_text):
    # Tokenize
    tokens = word_tokenize(raw_text)
    tokens = [token.lower() for token in tokens if token.isalpha() and
              token not in stopwords.words('english') and
              len(token) > 5]

    # Lemmatize
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    unique_lemmas = list(set(lemmas))

    # POS Tagging in unique_lemmas
    tags = pos_tag(unique_lemmas)
    print('\nFirst 20 tagged items in unique_lemmas: ')
    for i in range(0, 20):
        print(tags[i])

    # List of nouns in lemmas:
    tags = pos_tag(lemmas)
    nouns = []
    for token, pos in tags:
        if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
            nouns.append(token)

    print('\nNumber of tokens: ', len(tokens))
    print('Number of nouns in lemmas: ', len(nouns))

    return tokens, nouns


# Guessing game function
def guessing_game(top50):
    score = 5
    print("\n\nLet's play a word of guessing game!")
    print('Starting score: 5')

    rand_number = random.randint(0, 49)
    word = top50[rand_number]
    print(word, rand_number)

    letter = ''
    characters = []
    for char in word:
        characters.append('_')

    while letter != '!' and score >= 0:
        print(*characters, sep=' ')
        letter = input('\nGuess a letter: ')
        i = 0
        guess_right = False
        for char in word:
            if char == letter:
                characters[i] = letter
                i += 1
                guess_right = True
            else:
                i += 1
        if guess_right:
            score += 1
            print('Right !, Score is', score)
        else:
            score -= 1
            if score >= 0:
                print('Sorry, guess again. Score is', score)
            else:
                print('\nOh no! You lost')
        
# main
def main():
    # Method to handle the filepath in both Window and Mac
    def read_file(filepath):
        with open(os.path.join(os.getcwd(), filepath), 'r') as f:
            input_file = f.read()
        return input_file

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        raw_text = read_file(fp)

        # Calculate the lexical diversity
        tokens = word_tokenize(raw_text)
        unique_tokens = set(tokens)
        print('Lexical diversity: %.2f' % (len(unique_tokens) / len(tokens)))

        tokens, nouns = text_processing(raw_text)

        # Make dictionary{noun: count number of noun in tokens)
        nouns_dict = {}

        for noun in nouns:  # Initial the dictionary. Remove the duplicate
            if noun not in nouns_dict:
                nouns_dict[noun] = 0

        for token in tokens:  # Count of noun in tokens
            if token in nouns_dict:
                nouns_dict[token] += 1

        i = 0
        top50 = []
        print('\nThe 50 most common word:')
        for noun in sorted(nouns_dict, key=nouns_dict.get, reverse=True):
            print(noun, ':', nouns_dict[noun])
            top50.append(noun)
            i += 1
            if i >= 50:
                break

        # Guessing Game
        guessing_game(top50)

        word = 'test'
        lista = ['_', 't', '_', 'e']
        print(*word, sep=' ')
        print(*lista, sep=' ')
        word = 'test1'
        print(*word, sep=' ')


if __name__ == "__main__":
    main()
