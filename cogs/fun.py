import codecs
import discord
import os
import random
from .utils import arg_parse
from .utils import markdown
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='kaomoji', aliases=['km', 'kao'], hidden=True)
	async def _kaomoji(self, ctx):
		""" Output a random kaomoji"""
		emotion = ""
		valid_emotions = []
		pwd = os.path.dirname(os.path.realpath(__file__))

		try:
			for r, d, f in os.walk(os.path.join(pwd, "../data/kaomoji")):
				valid_emotions = f
			emotion = arg_parse.parse(ctx.message.content)[0]
		except:
			pass

		if emotion in valid_emotions:
			with open(os.path.join(pwd, "../data/kaomoji", emotion), 'r', encoding='utf-8') as f:
				lines = f.readlines()
				random_line = random.choice(lines)
		else:
			with open(os.path.join(pwd, "../data/kaomoji/sad"), 'r', encoding='utf-8') as f:
				lines = f.readlines()
				random_line = markdown.quote("That emotion could not be found {}".format(random.choice(lines)))

		await ctx.send(random_line)

def setup(bot):
	bot.add_cog(Fun(bot))