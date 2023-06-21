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


def get_weather():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=-33.86&longitude=151.21&daily=weathercode,temperature_2m_max,temperature_2m_min,sunset,rain_sum,showers_sum,precipitation_probability_max,windspeed_10m_max&current_weather=true&forecast_days=1&timezone=Australia%2FSydney'
    response = requests.get(url)
    weather_data = response.json()

    weathercodes = {0:'Clear sky', 1:'Mainly clear', 2:'Partly cloudy', 3:'Overcast', 45:'Fog', 51:'Light drizzle', 53:'Moderate drizzle', 55:'Heavy drizzle', 61:'Light rain', 63:'Moderate rain', 65:'Heavy rain', 80:'Light  showers', 81:'Moderate showers', 82:'Heavy showers'}
    
    time_ls = weather_data['current_weather']['time'].split('T')
    current_time = time_ls[1]

    output = "Weather in Sydney on " + weather_data['daily']['time'][0] + " at " + current_time + "\n"
    if weather_data['daily']['weathercode'][0] not in weathercodes:
        output += "Strange weather!" + "\n"
    output += weathercodes[weather_data['daily']['weathercode'][0]] + "\n"
    output += "Current temperature: " + str(weather_data['current_weather']['temperature']) + "\u00B0C\n"
    output += "Current wind speed: " + str(weather_data['current_weather']['windspeed']) + "km/h\n"
    output += "Rain: " + str(weather_data['daily']['rain_sum'][0]) + "mm\n"
    output += "Showers: " + str(weather_data['daily']['showers_sum'][0]) + "mm\n"
    output += "Max chance of precipitation: " + str(weather_data['daily']['precipitation_probability_max'][0]) + " %"

    return output


