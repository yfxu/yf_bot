import discord
import json
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
from .utils import arg_parse

load_dotenv()

class Osu(commands.Cog):
	"""osu! cog"""
	def __init__(self, bot):
		self.bot = bot
		self.api_key = os.getenv('OSU_TOKEN')


	# ------------------- common osu functions ------------------- #

	# Return dictionary containing mode name and id
	def get_mode_id(self, osu_mode):
		osu_mode = str(osu_mode)

		if osu_mode.lower() == "taiko" or osu_mode.lower() == "t" or osu_mode == "1":
			return { "name": "osu!taiko", "id": 1 }
		elif osu_mode.lower() == "catch" or osu_mode.lower() == "c" or osu_mode.lower() == "ctb" or osu_mode == "2":
			return { "name": "osu!catch", "id": 2 }
		elif osu_mode.lower() == "mania" or osu_mode.lower() == "m" or osu_mode == "3":
			return { "name": "osu!mania", "id": 3 }
		else: 
			return { "name": "osu!std", "id": 0 }

	# Fetch get_user from osu! api v1
	def get_user_info(self, osu_user_id, osu_mode_id=0):
		return requests.get("https://osu.ppy.sh/api/get_user", params={'k': self.api_key, 'u': osu_user_id, 'm': osu_mode_id}).json()[0]

	
	# ------------------- osu! discord commands ------------------- #

	# Output embed with basic osu player stats
	@commands.command(name="osu")
	async def _get_osu_user(self, ctx):
		try:
			args = arg_parse.parse(ctx.message.content)
		except:
			await ctx.send("No user was provided")

		try:
			osu_user_id = args[0]
			osu_mode = self.get_mode_id(args[1])
		except:
			osu_user_id = args[0]
			osu_mode = self.get_mode_id(0)

		r = self.get_user_info(osu_user_id, osu_mode['id'])

		embed = discord.Embed(
			title = ":flag_{}:  {}  (#{})  ({}#{})".format(r['country'].lower(), r['username'], r['pp_rank'], r['country'], r['pp_country_rank']), 
			colour = discord.Colour(0xfcba03),
			description = """**Total PP:**  {}
			**Accuracy:**  {}%
			**Playcount:**  {}
			**Join date:**  {}
			""".format(r['pp_raw'], "{:.2f}".format(float(r['accuracy'])), r['playcount'], r['join_date'])
		)
		embed.set_thumbnail(url = "https://a.ppy.sh/{}".format(r['user_id']))
		embed.set_footer(text = "{} profile for {}".format(osu_mode['name'], r['username']))

		await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(Osu(bot))