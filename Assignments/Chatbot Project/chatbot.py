# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002
#         Amol Perubhatla - AVP180003

# Porfolio: Chatbot Project

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

NUM_IMPORTANT_TERM = 25

def send_message(answer):
    bot_template = "Bot : {0}"
    print(bot_template.format(answer))


def chatbot_respond(user_input, k_base):
    # Add the user input into knowledge base
    k_base.append(user_input)

    # Create the tfidf vector from knowledge_base
    vectorizer = TfidfVectorizer()
    sentences_tfidf = vectorizer.fit_transform(k_base)

    # Calculate the similarity of user_input and sentences in knowledge_base
    # sentences_vectors[-1] is the user_input after TfidfVectorizer
    similarity_score = cosine_similarity(sentences_tfidf[-1], sentences_tfidf)

    i = 3
    prev = k_base[similarity_score.argsort()[0][-2]]  # Base case
    answers = [prev]

    num_answer = 0
    while i <= len(similarity_score.argsort()[0]) and num_answer < 5:
        current = k_base[similarity_score.argsort()[0][-i]]
        if current != prev:
            answers.append(current)
            prev = current
            i += 1
            num_answer += 1
        else:
            i += 1

    # print('Answer List') # debug
    # print(*answers, sep="\n") # debug

    # Check if we have related answer from knowledge_base
    similar = similarity_score.flatten() # Convert to 1-dim vector
    similar.sort()
    if similar[-2] == 0:
        return answers.clear()
    else:
        return answers

# main
def main():

    # user_name will contain: name and information relevant to users
    user_name = input("Please enter your username:").lower()

    print('Chatbot initialize ...')

    # Handpick important term on knowledge base
    top15 = ['cyberpunk', 'high tech-low life', 'blade runner', 'matrix', 'william gibson',
             'corporation', 'mega city', 'philosophy']

    try:  # open user profile
        # read the pickle file
        dict_username = pickle.load(open('dict_username.p', 'rb'))  # read binary
        # print(dict_username) # debug
    except FileNotFoundError:
        dict_username = {}

    try:  # open knowledge base
        # read the pickle file
        k_base = pickle.load(open('k_base.p', 'rb'))  # read binary

    except FileNotFoundError:
        # Create knowledge base
        call(["python", "knowledge_base.py"])
        k_base = pickle.load(open('k_base.p', 'rb'))  # read binary

    exit_template = ["stop", "exit"]

    print('\n************\n')
    bot_template = "Bot : {0}"

    if user_name in dict_username:  # User already exist
        name = dict_username.get(user_name)[0].title()
        exist_user_greeting = "Hi " + name + ". " + "Good to see you again !"
        print(bot_template.format(exist_user_greeting))
        while True:
            user_input = input(name.title() + ' : ').lower()
            if user_input in exit_template:
                break
            # related_text = related(user_input)
            answers = chatbot_respond(user_input, k_base)
            if answers is not None:
                send_message(random.choice(answers))
                k_base.remove(user_input)
            else:
                suggestions = "Sorry. I am not sure what you mean. Try: " + str(top15)
                print(bot_template.format(suggestions))

    else:  # New user. Build new profile
        new_user_greeting = "Hi there! What should i call you?"
        print(bot_template.format(new_user_greeting))
        name = input('User : ').lower()
        dict_username[user_name] = [name]

        while True:
            user_input = input(name.title() + ' : ').lower()
            if user_input in exit_template:
                break
            answers = chatbot_respond(user_input, k_base)
            if answers is not None:
                send_message(random.choice(answers))
                k_base.remove(user_input)
            else:
                suggestions = "Sorry. I am not sure what you mean. Try: " + str(top15)
                print(bot_template.format(suggestions))


    # save the pickle file before exit program
    pickle.dump(dict_username, open('dict_username.p', 'wb'))  # write binary


if __name__ == "__main__":
    main()
