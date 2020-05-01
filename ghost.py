import os
import discord
import datetime
from due import Due
import schedule
import time


# extract a due
def interpretDue(dueText):
    sliced = dueText.split("/")
    sliced.append(sliced[3][3:])
    newDue = Due(
        date = datetime.datetime(
            int('20'+sliced[3][0:2]),int(sliced[2]),int(sliced[1]),hour = int(sliced[0])
            ),
        text = sliced[4]
        )
    return newDue

# dump a due
def dumpDue(theDue):
    return f'{theDue.date.strftime("%H")}/{theDue.date.strftime("%d")}/{theDue.date.strftime("%m")}/{theDue.date.strftime("%y")} {theDue.text}'

# convert due to good looking discord message
def visualDue(theDue):
    now = datetime.datetime.now()
    remain = theDue.date - now
    if remain.days < 0 : return False
    statusEmoji = ''
    if remain.days > 7: statusEmoji = ':ok_hand:'
    elif remain.days > 1: statusEmoji = ':warning:'
    else: statusEmoji = ':sos:'
    visualized = statusEmoji + f'**{theDue.text}** '
    if remain.days != 0: visualized = visualized + f'{remain.days}d '
    if remain.seconds > 3600:
        inSec = remain.seconds
        inHour = divmod(inSec, 3600)[0]
        inSec = divmod(inSec, 3600)[1]
        visualized = visualized + f'{inHour}h '
    if inSec > 60:
        inMin = divmod(inSec, 60)[0]
        inSec = divmod(inSec, 60)[1]
        visualized = visualized + f'{inMin}min '
    if inSec > 0:
        visualized = visualized + f'{inSec}s '
    visualized = visualized + 'remaining\n\n'
    return visualized

# Read bot and guild tokens
f = open("env_real" , "r")
token = f.readline()
guildId = f.readline()
f.close()

# Load saved due list
# exp line: 16/07/05/20 Dsa
f = open("dues.gdl" , "r")
duesRaw = f.readlines()
dues = []
for line in duesRaw:
    dues.append(interpretDue(line))
f.close()

# Create client instance and connect
client = discord.Client()
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id == int(guildId.rstrip()):
            break

    print(f'{client.user} successful connected to {guild.name}')

# Event when message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    respond = check_message(message.content)
    if respond != False :
        richText = discord.Embed(description=respond, color=discord.Color.gold())
        await message.channel.send(embed=richText)

# Handle message
def check_message(msg):
    if not (msg[0:5].lower() == 'ghost'): return False
    msgQuery = msg[6:].split(" ")
    if msgQuery[0] == 'show': 
        reply = ''
        for everyDue in dues[:]:
            visualDueTemp = visualDue(everyDue)
            if visualDueTemp == False :
                dues.remove(everyDue)
            else: 
                reply = reply + visualDueTemp
        return reply
    if msgQuery[0] == 'add': 
        dues.append(interpretDue(msgQuery[1] + ' ' + msgQuery[2]))
        f = open("dues.gdl" , "w")
        for line in dues:
            f.write(dumpDue(line).rstrip("\n") + '\n')
        f.close()
        return 'success'
    if msgQuery[0] == 'clear':
        f = open("dues.gdl" , "w")
        f.close()
        dues.clear()
        return 'success'

client.run(token)
