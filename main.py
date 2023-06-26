import guess_the_number
import apis
import database
import stats

import discord
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

    if msg == "!weather":
        weather = apis.get_weather()
        await message.channel.send(weather)

    if msg == "!initialise":
        database.initialise_db()
    
    if msg.startswith("!addPlayer"):
        name = msg.replace("!addPlayer ", "")
        database.add_player(name)

    if msg.startswith("!getPlayer"):
        name = msg.replace("!getPlayer ", "")
        player = database.get_player(name)
        name = player[0][0]
        wins = str(player[0][1])
        losses = str(player[0][2])

        if player:
            string = name + "\n" + "Wins: " + wins + "\n" + "Losses: " + losses
            await message.channel.send(string)
        else:
            await message.channel.send("Player does not exist in database")

    if msg.startswith("!getTeam"):
        names = msg.replace("!getTeam ", "")
        names = names.split(" ")
        if len(names) != 2:
            await message.channel.send("Wrong format")
        
        team = database.get_team(names[0], names[1])
        wins = str(team[0][2])
        losses = str(team[0][3])

        if team:
            string = team[0][0] + ", " + team[0][1] + "\n" + "Wins: " + wins + "\n" + "Losses: " + losses
            await message.channel.send(string)
        else:
            await message.channel.send("Team does not exist in database")

    if msg.startswith("!gameResult"):
        msg = msg.replace("!gameResult ", "")
        msg_split = msg.split(" ")
        
        try:
            name_1 = msg_split[0]
            name_2 = msg_split[1]
            wins = int(msg_split[2].split("-")[0])
            losses = int(msg_split[2].split("-")[1])
            
            database.update_team_scores(name_1, name_2, wins, losses)
            database.update_individual_scores(name_1, name_2, wins, losses)
            await message.channel.send("Scores updated")
        except IndexError:
            await message.channel.send("Wrong format")
  
    if msg.startswith("!winrate"):
        msg = msg.replace("!winrate ", "")
        msg_split = msg.split(" ")
        if len(msg_split) > 2 or len(msg_split) <= 0:
            await message.channel.send("Wrong format")
            return
        
        # Player
        if len(msg_split) == 1:
            win_rate = stats.get_player_win_rate(msg_split[0])
            if win_rate:
                win_rate_str = str(win_rate) + "%"
                await message.channel.send(win_rate_str)
            else:
                await message.channel.send("Player does not exist in the database")
        # Team
        else:
            win_rate = stats.get_team_win_rate(msg_split[0], msg_split[1])
            if win_rate: 
                win_rate_str = str(win_rate) + "%"                                   
                await message.channel.send(win_rate_str)
            else:
                await message.channel.send("Team does not exist in the database")

    if msg == "!bestTeam":
        name_1, name_2, win_rate = stats.get_best_team()
        string = name_1 + ", " + name_2 + "\n" + "Win rate: " + str(win_rate) + "%"
        await message.channel.send(string)

    if msg == "!worstTeam":
        name_1, name_2, win_rate = stats.get_worst_team()
        string = name_1 + ", " + name_2 + "\n" + "Win rate: " + str(win_rate) + "%"
        await message.channel.send(string)


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
        if scheduled_time < datetime.now():
            await channel.send("Invalid time")
            return

        while datetime.now() < scheduled_time:
            await asyncio.sleep(1)
    except ValueError:
        await channel.send("Invalid time")
        return
        
    await channel.send("notification")


client.run("TOKEN")  # replace TOKEN with the actual token
