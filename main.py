import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.user)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('hello LabBot'):
        await message.channel.send("Hello " + message.author.name)

client.run("TOKEN")  # replace TOKEN with the actual token
