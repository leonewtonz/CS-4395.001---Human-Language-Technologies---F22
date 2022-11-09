# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002

# Porfolio: Chatbot Project
import random


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


def send_message(message, user_name):
    bot_template = "Bot : {0}"
    response = respond(message)
    print(bot_template.format(response))


# main
def main():
    user_name = input("Please enter your username:")
    user_name = user_name.lower()

    # key = user_name
    # value = [name, personal info, like, dislike, personal remarks]

    # personal remarks: top 20 word in the whole conversation (Current and Past, each for each text)

    ## like/dislike: tokens, sentences --> anything after that word
    dict_username = {}

    print('\n************\n')
    bot_template = "Bot : {0}"

    exist_user_greeting = "Hi " + user_name + "!. " + "Good to see you again"
    new_user_greeting = "Hi there! What should i call you?"

    if user_name in dict_username:
        print(bot_template.format(exist_user_greeting))
        # open pickle
    # get everything ready for conservation
    else:  # New user. Build new profile
        print(bot_template.format(new_user_greeting))
        name = input('User : ').lower()
        dict_username[user_name] = [name]

        # dict_username[user_name].append('123')
        # print('Name of user:' + dict_username[user_name][1])  # debug

        while True:
            user_input = input(name.title() + ' : ')
            if user_input == "exit" or user_input == "stop":
                break
            related_text = related(user_input)
            send_message(related_text, user_name)


    # while True:
    #     user_input = input(user_name + ' : ')
    #     user_input = user_input.lower()
    #     related_text = related(user_input)
    #     send_message(related_text, user_name)
    #     if user_input == "exit" or user_input == "stop":
    #         break


if __name__ == "__main__":
    main()
