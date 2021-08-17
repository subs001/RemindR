import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
from datetime import date

today = date.today()
today = today.strftime("%d/%m/%Y")

load_dotenv()

client = discord.Client()
bot = commands.Bot(command_prefix='$')

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

@bot.command(name='remind')
async def getDate(ctx):

    # function to check if the confirmation message was sent by the same user
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
        
    if ctx.author == client.user:
        return
    
    await ctx.channel.send('Hi, this is RemindR!')
    await ctx.send('Enter the date in the d/m/y format along with the title of the reminder')
    message = await bot.wait_for("message", check=check)

    content = message.content.split(' ',1)
    if(len(content) == 2):
        if(checkDate(content[0])):
            await message.channel.send('Do you want to set a reminder at: ' + content[0] + '?(yes/no)')
            confirmation = await bot.wait_for("message", check=check)
            if(confirmation.content.lower() == 'yes'):
                await message.channel.send("Reminder Set!")
            else:
                await message.channel.send("Reminder Not Set!")
                return
        else:
            await message.channel.send('Invalid Syntax')
            

TOKEN = os.environ['TOKEN']
bot.run(TOKEN)