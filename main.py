import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
from datetime import date
import random
from discord import Intents
load_dotenv()
intents = Intents.all()
client = discord.Client()
bot = commands.Bot(command_prefix='$', intents=intents)

# global variables
reminderObject = dict()
reaction_list = []
today = date.today()
today = today.strftime("%d/%m/%Y")

# function to create object to be stored in the databse
def createObject(ID, dateRequired, title):
    reminderObject[ID] = {
        "user": {},
        "date": dateRequired,
        "title": title
    }

# function to check if date entered is in the correct format
def checkDate(input):
    try:
        datetime.datetime.strptime(input,"%d/%m/%Y")
        return True
    except ValueError as err:
        return False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# command to set reminders
@bot.command(name='remind')
async def getDate(ctx):

    # function to check if the confirmation message was sent by the same user
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
        
    # ensuring bot doesn't reply to its own messages    
    if ctx.author == client.user:
        return
    
    await ctx.channel.send('Hi, this is RemindR!')
    await ctx.send('Enter the date in the d/m/y format along with the title of the reminder')
    message = await bot.wait_for("message", check=check)

    # split message into date and title of the reminder
    content = message.content.split(' ',1)
    if(len(content) == 2):
        if(checkDate(content[0])):
            await message.channel.send('Do you want to set a reminder at: ' + content[0] + '?(yes/no)')
            confirmation = await bot.wait_for("message", check=check)
            if(confirmation.content.lower() == 'yes'):
                # sending username in the form of NAME#ID, similar to how discord identifies users
                reactionMessage = await ctx.send("Reminder Set!\n**React '???' to this message to sign up!**")
                await reactionMessage.add_reaction("????")
                await reactionMessage.add_reaction("????")
                # an object is created, and its unique ID is the same as that of the reaction message's
                createObject(reactionMessage.id, content[0], content[1])
            else:
                await message.channel.send("Reminder Not Set!")
                return
        else:
            await message.channel.send('Invalid Syntax')


# this event listens for user reactions and adds them to the reminderObject structure to subscribe them to that reminder
@bot.event
async def on_raw_reaction_add(payload):
    reactedUser = payload.member.id  
    reactedEmoji = payload.emoji.name
    if(payload.member.display_name != "RemindR"):
        if(reactedEmoji == '????'):
            # reactedUser = reactedUser + '#' + payload.member.discriminator
            reminderObject[payload.message_id]["user"][reactedUser] = "Incomplete"
        elif(reactedEmoji == '????'):
            reminderObject[payload.message_id]["user"][reactedUser] = "Complete"

# command to mention users who have subscribed to a reminder
@bot.command(name='show')
async def showUsers(ctx):
    for key in reminderObject:
        for user in reminderObject[key]['user']:
            await ctx.channel.send('<@' + str(user) + '>')
        

TOKEN = os.environ['TOKEN']
bot.run(TOKEN)