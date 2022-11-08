# CS 4395.001 - NLP
# Dr. Karen Mazidi
# Author: Leo Nguyen - ldn190002

# Porfolio: Chatbot Project
import random


def related(x_text):
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

    print('\n************\n')
    bot_template = "Bot : {0}"

    greet1 = "Hi " + user_name + "!. " + "Good to see you again"
    print(bot_template.format(greet1))

    while True:
        user_input = input(user_name + ' : ')
        user_input = user_input.lower()
        related_text = related(user_input)
        send_message(related_text, user_name)
        if user_input == "exit" or user_input == "stop":
            break


if __name__ == "__main__":
    main()
