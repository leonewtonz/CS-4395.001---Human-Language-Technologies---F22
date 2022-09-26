# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen
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

    # Lower-case raw text
    # Reduce tokens to only those that are alpha
    # Not in the NLTK stopwords
    # Have length > 5
    tokens = [token.lower() for token in tokens if token.isalpha() and
              token not in stopwords.words('english') and
              len(token) > 5]

    # Lemmatize
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    unique_lemmas = list(set(lemmas))  # Make unique

    # POS Tagging the unique_lemmas
    tags = pos_tag(unique_lemmas)
    print('\nFirst 20 tagged items in unique_lemmas: ')
    for i in range(0, 20):
        print(tags[i])

    # List of nouns in lemmas
    # This nouns list will content duplicate elements.
    # It is because many words will end up in the same form.
    # after we lemmatize the tokens. For example: 'contraction'. Check Debug 1

    # Nouns mean any word have tags: NN, NNS, NNP, NNPS
    # tags = pos_tag(lemmas)
    nouns = []
    for token, pos in tags:
        if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
            nouns.append(token)

    # print('Content of nouns: ', nouns[:10]) #___Debug 1___#
    print('\nNumber of tokens: ', len(tokens))
    print('Number of nouns in unique_lemmas: ', len(nouns))

    return tokens, nouns


# Guessing game function
def guessing_game(top50):
    score = 5  # Starting points
    print("\n\nLet's play a word of guessing game!")
    print('Starting score: 5')

    # Create a random number from 0-49 inclusive.
    # These number 0-49 will be used as index to pick word from top50
    rand_number = random.randint(0, 49)
    word = top50[rand_number]
    # print(word, rand_number) # Debug 2

    letter = ''  # Container for input letter
    characters = []  # Container for 'ongoing' word. Use to check the progress of the game
    for char in word:  # Initialize with "underscore space" and print them out
        characters.append('_')
    print(*characters, sep=' ')

    while letter != '!' and score >= 0: # Game end when score negative or user enter '!'
        # Word guess correctly.
        # Let user know.
        # Show current score.
        # Game continue with another random word from top50
        if '_' in characters:
            letter = input('\nGuess a letter: ')
            if letter == '!':  # Game end when user enter '!'
                break
            else:  # Game in progress.
                if letter not in characters:
                    i = 0
                    guess_right = False
                    for char in word:
                        if char == letter:
                            characters[i] = letter  # Save correctly guessed letter in characters
                            i += 1  # Move to next index in characters list
                            guess_right = True
                        else:
                            i += 1

                    # Calculate the score and output feedback for user
                    if guess_right:
                        score += 1
                        print('Right! Score is', score)
                        print(*characters, sep=' ')
                    else:
                        score -= 1
                        if score >= 0:
                            print('Sorry, guess again. Score is', score)
                            print(*characters, sep=' ')
                        else:
                            print('\n________YOU LOSE________')
                else:
                    # Prevent increasing score when user re-input correctly guessed letter
                    print('Letter', letter, ': has been discovered. Score is', score)
        else:
            print('\n________YOU SOLVED IT________')
            print('Current score:', score)
            print('\nGuess another word')

            rand_number = random.randint(0, 49)
            word = top50[rand_number]
            print(word, rand_number)

            characters = []
            for char in word:
                characters.append('_')
            print(*characters, sep=' ')


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

        # Preprocessing
        tokens, nouns = text_processing(raw_text)

        # Make dictionary{noun: count number of noun in tokens)
        nouns_dict = {}

        # Initialize count=0 for nouns dictionary.
        # Nouns list already a unique set as it was extract from unique_lemmas
        for noun in nouns:
                nouns_dict[noun] = 0

        # Count of noun in tokens
        for token in tokens:
            if token in nouns_dict:
                nouns_dict[token] += 1

        # Print out the 50 most common words and save to top50 list
        i = 0
        top50 = []
        print('\nThe 50 most common words:')
        for noun in sorted(nouns_dict, key=nouns_dict.get, reverse=True):
            print(noun, ':', nouns_dict[noun])
            top50.append(noun)
            i += 1
            if i >= 50:
                break

        # Guessing Game
        guessing_game(top50)


if __name__ == "__main__":
    main()
