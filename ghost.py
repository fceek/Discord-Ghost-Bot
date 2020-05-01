import os
import discord

f = open("env_real" , "r")
token = f.readline()
guildId = f.readline()
f.close()

client = discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == guildId:
            break

    print(f'{client.user} successful connected to {guild.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    respond = '?'

    if check_mention(message.content):
        await message.channel.send(respond)

def check_mention(msg):
    keywords = ['bot','jiqiren','ji qi ren','机器人']
    for v in keywords:
        if v in msg.lower():
            return True
    return False

client.run(token)