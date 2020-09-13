import os
import discord
import tweepy

from .utils import arg_parse
from discord.ext import commands
from dotenv import load_dotenv

# import authentication credentials
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

class Twitter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	""" Tweet Generator """
	@commands.command(name='gen', hidden=True)
	async def _gen(self, ctx):
		acc_tag = arg_parse.parse(ctx.message.content)[0]

		# authentic bot for Twitter API access
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)

		# print user's last 10 tweets
		for tweet in tweepy.Cursor(api.user_timeline, user_id=acc_tag.strip('@'), tweet_mode='extended').items(10):
			print(tweet.full_text)

def setup(bot):
	bot.add_cog(Twitter(bot))