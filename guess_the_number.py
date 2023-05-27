import random


def start_game():
    return random.randint(1, 10)


def run(inpt, num):
    if inpt > num:
        return "Guess lower"
    elif inpt < num:
        return "Guess higher"
    else:
        return "You are correct! " + str(inpt) + " was the number."
