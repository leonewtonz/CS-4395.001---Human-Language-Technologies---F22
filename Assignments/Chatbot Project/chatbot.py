# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002

# Porfolio: Chatbot Project

import random
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def related(x_text):
    x_text = x_text.lower()
    if "name" in x_text:
        y_text = "what's your name?"
    elif "weather" in x_text:
        y_text = "what's today's weather?"
    elif "robot" in x_text:
        y_text = "Are you a robot?"
    elif "how are" in x_text:
        y_text = "How are you?"
    else:
        y_text = ""
    return y_text


def respond(message):
    name = "Funny Bot 101"
    weather = "rainy"
    mood = "Happy"
    responses = {
        "what's your name?": [
            "They call me {0}".format(name),
            "I usually go by {0}".format(name),
            "My name is the {0}".format(name)],
        "what's today's weather?": [
            "The weather is {0}".format(weather),
            "It's {0} today".format(weather),
            "Let me check, it looks {0} today".format(weather)],
        "Are you a robot?": [
            "What do you think?",
            "Maybe yes, maybe no!",
            "Yes, I am a robot with human feelings.", ],
        "How are you?": [
            "I am feeling {0}".format(mood),
            "{0}! How about you?".format(mood),
            "I am {0}! How about yourself?".format(mood), ],
        "": [
            "Hey! Are you there?",
            "What do you mean by saying nothing?",
            "Sometimes saying nothing tells a lot :)", ],
        "default": [
            "this is a default message"]}

    if message in responses:
        bot_message = random.choice(responses[message])
    else:
        bot_message = random.choice(responses["default"])
    return bot_message


def send_message(answer):
    bot_template = "Bot : {0}"
    print(bot_template.format(answer))


def chatbot_respond(user_input, k_base):
    # Append the query to the sentences list
    k_base.append(user_input)
    # Create the sentences vector based on the list
    vectorizer = TfidfVectorizer()
    sentences_vectors = vectorizer.fit_transform(k_base)

    # Measure the cosine similarity and take the second closest index because the first index is the user query
    vector_values = cosine_similarity(sentences_vectors[-1], sentences_vectors)
    answer = k_base[vector_values.argsort()[0][-2]]
    # Final check to make sure there are result present. If all the result are 0, means the text input by us are not captured in the corpus
    input_check = vector_values.flatten()
    input_check.sort()

    if input_check[-2] == 0:
        return "Please Try again"
    else:
        return answer

# main
def main():
    # os.system('python az.py') # debug
    user_name = input("Please enter your username:").lower()

    # key = user_name
    # value = [name, personal info, like, dislike, personal remarks]

    # personal remarks: top 20 word in the whole conversation (Current and Past, each for each text)

    ## like/dislike: tokens, sentences --> anything after that word

    try:
        # read the pickle file
        dict_username = pickle.load(open('dict_username.p', 'rb'))  # read binary
        # print(dict_username) # debug
    except FileNotFoundError:
        dict_username = {}


    try:
        # read the pickle file
        k_base = pickle.load(open('k_base.p', 'rb'))  # read binary
        # print(dict_username) # debug
    except FileNotFoundError:
        # Maybe run the knowledge base file
        pass


    print('\n************\n')
    bot_template = "Bot : {0}"

    if user_name in dict_username: # User already exist
        name = dict_username.get(user_name)[0].title()
        exist_user_greeting = "Hi " + name + ". " + "Good to see you again !"
        print(bot_template.format(exist_user_greeting))
        while True:
            user_input = input(name.title() + ' : ').lower()
            if user_input == "exit" or user_input == "stop":
                break
            # related_text = related(user_input)
            answer = chatbot_respond(user_input, k_base)
            send_message(answer)




    # get everything ready for conservation
    else:  # New user. Build new profile
        new_user_greeting = "Hi there! What should i call you?"
        print(bot_template.format(new_user_greeting))
        name = input('User : ').lower()
        dict_username[user_name] = [name]

        # dict_username[user_name].append('123')
        # print('Name of user:' + dict_username[user_name][1])  # debug

        while True:
            user_input = input(name.title() + ' : ').lower()
            if user_input == "exit" or user_input == "stop":
                break
            answer = chatbot_respond(user_input, k_base)
            send_message(answer)

    # save the pickle file before exit program
    pickle.dump(dict_username, open('dict_username.p', 'wb'))  # write binary

    # while True:
    #     user_input = input(user_name + ' : ')
    #     user_input = user_input.lower()
    #     related_text = related(user_input)
    #     send_message(related_text, user_name)
    #     if user_input == "exit" or user_input == "stop":
    #         break


if __name__ == "__main__":
    main()
