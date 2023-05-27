import discord
import guess_the_number

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
            output = guess_the_number.run(int(msg), num)
            if output == "You are correct! " + msg + " was the number.":
                game = ""
            await message.channel.send(output)

    if msg == "Hello LabBot":
        await message.channel.send("Hello " + message.author.name + '!')

    if msg == "!guess":
        await message.channel.send("Guess the number from 1-10")
        num = guess_the_number.start_game()
        game = "gtn"


client.run("TOKEN")  # replace TOKEN with the actual token
