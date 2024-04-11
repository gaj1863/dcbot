import discord
from discord.ext import commands
import json
import os


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, owner_id=543290770283692042)

bot.remove_command('help')



@bot.event
async def on_ready(): 
    print(">> Bot is Online! <<")

    

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}') 



with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)


if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
