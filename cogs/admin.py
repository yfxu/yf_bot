import os
import discord

from .utils import arg_parse
from discord.ext import commands
from dotenv import load_dotenv

# import author id
load_dotenv()
AUTHOR_ID = os.getenv('AUTHOR_ID')

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def is_owner(ctx):
		return ctx.author.id == AUTHOR_ID

	@commands.command(name='reload', hidden=True)
	@commands.check(is_owner)
	async def _reload(self, ctx):
		"""Reloads a module."""
		try:
			module = "cogs." + arg_parse.parse(ctx.message.content)[0]
			self.bot.reload_extension(module)
		except Exception as e:
			await ctx.send('{}: {}'.format(type(e).__name__, e))
		else:
			await ctx.send("{} module successfully reloaded!".format(module))


	@commands.command(name='load', hidden=True)
	@commands.check(is_owner)
	async def _load(self, ctx):
		"""Loads a module."""
		try:
			module = "cogs." + arg_parse.parse(ctx.message.content)[0]
			self.bot.load_extension(module)
		except Exception as e:
			await ctx.send('{}: {}'.format(type(e).__name__, e))
		else:
			await ctx.send("{} module successfully loaded!".format(module))

def setup(bot):
	bot.add_cog(Admin(bot))