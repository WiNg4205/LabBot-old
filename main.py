import discord
import guess_the_number
import apis
import threading
import asyncio
from datetime import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True  

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.user)

game = ""
num = 0

@client.event
async def on_message(message):
    global game, num
    if message.author == client.user:
        return

    msg = message.content

    if game != "":
        if game == "gtn":
            if msg.isdigit():
                output = guess_the_number.run(int(msg), num)
                if output == "You are correct! " + msg + " was the number.":
                    game = ""
                await message.channel.send(output)

    if msg == "Hello LabBot":
        await message.channel.send("Hello " + message.author.name + '!')

    if msg == "!inspire":
        quote = apis.get_quote()
        await message.channel.send(quote)

    if msg == "!joke":
        joke = apis.get_joke()
        await message.channel.send(joke)

    if msg == "!ejoke":
        joke = apis.get_explicit_joke()
        await message.channel.send(joke)

    if msg == "!guess":
        await message.channel.send("Guess the number from 1-10")
        num = guess_the_number.start_game()
        game = "gtn"

    if msg.startswith("!setNotification"):
        await send_notification(msg)


async def send_notification(msg):
    msg = msg.replace("!setNotification ", "")
    date_time = msg.split(" ")
    date_ls = date_time[0].split("-")
    time_ls = date_time[1].split(":")

    channel = client.get_channel(1109277709806338090)

    if (len(date_ls) != 3) or (len(time_ls) != 3):
        await channel.send("Wrong format")
        return
    
    try:
        scheduled_time = datetime(int(date_ls[2]), int(date_ls[1]), int(date_ls[0]), int(time_ls[0]), int(time_ls[1]), int(time_ls[2]))
        while datetime.now() < scheduled_time:
            await asyncio.sleep(1)
    except ValueError:
        await channel.send("Invalid time")
        return
        
    await channel.send("notification")


client.run("MTExMTgwMDkxNjU4OTQzMjkwNg.GPUKV-.cCcYBeFtoV94kOeLW-BQwPc5eoGchMTX5h4PKw")  # replace TOKEN with the actual token
