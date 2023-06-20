import json

import requests


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    # concat quote and author
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote


def get_joke():
    url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist'
    response = requests.get(url)
    joke_data = response.json()

    if joke_data['type'] == 'single':
        joke = joke_data['joke']
    else:
        joke = f"{joke_data['setup']}\n{joke_data['delivery']}"
    return joke


def get_explicit_joke():
    url = 'https://v2.jokeapi.dev/joke/Any'
    response = requests.get(url)
    joke_data = response.json()

    if joke_data['type'] == 'single':
        joke = joke_data['joke']
    else:
        joke = f"{joke_data['setup']}\n{joke_data['delivery']}"
    return joke
