# yf_bot.py
import os
import discord

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

# discord token
load_dotenv()
DISCORD_TOKEN = os.getenv( 'DISCORD_TOKEN' )

bot = commands.Bot( command_prefix=".." )

# extensions for commands found in cogs folder
extensions = ['cogs.osu', 'cogs.admin', 'cogs.fun', 'cogs.gamble', 'cogs.twitter']
if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

@bot.event
async def on_message(message):
	if message.author != bot.user:
		#print( datetime.now().replace( microsecond=0 ), message.author, message.content )
		await bot.process_commands(message)

@bot.event
async def on_ready():
	print( f'{bot.user} has connected to Discord!' )


bot.run( DISCORD_TOKEN, bot=True, reconnect=True )
