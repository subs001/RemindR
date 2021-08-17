import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
from datetime import date
import random

today = date.today()
today = today.strftime("%d/%m/%Y")

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='$')

reminderObject = dict()

# function to create object to be stored in the databse
def createObject(username, dateRequired, title):
    objectID = random.randint(1000, 10000)
    reminderObject[objectID] = {
        "user": {
            username: "Incomplete"
        },
        "date": dateRequired,
        "title": title
    }
    return objectID

# function to check if date entered is in the correct format
def checkDate(input):
    try:
        datetime.datetime.strptime(input,"%d/%m/%Y")
        return True
    except ValueError as err:
        return False

# @client.event()
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

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
                ID = createObject(ctx.author.name + '#' + ctx.author.discriminator, content[0], content[1])
                await message.channel.send("Reminder Set! ID: " + str(ID))
            else:
                await message.channel.send("Reminder Not Set!")
                return
        else:
            await message.channel.send('Invalid Syntax')
            

# command to subsribe to an existing reminder
@bot.command(name='sub')
async def subscribe(ctx):

    # ensuring bot doesn't reply to its own messages    
    if ctx.author == client.user:
        return

    # function to check if the confirmation message was sent by the same user
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.channel.send('Enter the ID of the reminder')
    message = await bot.wait_for("message", check=check)
    ID = int(message.content)
    # check if the id exists
    if ID in reminderObject:
        reminderObject[ID]["user"][ctx.author.name + '#' + ctx.author.discriminator] = "Incomplete"
        print(reminderObject)
        await ctx.channel.send('Subscribed!')
    else:
        await ctx.channel.send('ID not found!')
        

TOKEN = os.environ['TOKEN']
bot.run(TOKEN)