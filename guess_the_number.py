import random


def start_game():
    return random.randint(1, 10)


def run(inpt, num):
    if inpt > num:
        if inpt > 10:
            return "Guess between 1-10"
        return "Guess lower"
    elif inpt < num:
        if inpt < 1:
            return "Guess between 1-10"
        return "Guess higher"
    else:
        return "You are correct! " + str(inpt) + " was the number."
