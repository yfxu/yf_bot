import os
import time
import discord
import tweepy

from .utils import arg_parse
from discord.ext import commands
from dotenv import load_dotenv

# import authentication credentials
load_dotenv()
CONSUMER_KEY = os.getenv( 'CONSUMER_KEY' )
CONSUMER_SECRET = os.getenv( 'CONSUMER_SECRET' )
ACCESS_KEY = os.getenv( 'ACCESS_KEY' )
ACCESS_SECRET = os.getenv( 'ACCESS_SECRET' )

class Twitter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	""" Tweet Generator """
	@commands.command( name='tweetgen', hidden=True )
	async def _tweetgen( self, ctx ):
		twitter_id = arg_parse.parse( ctx.message.content )[0].strip( '@' )

		# authentic bot for Twitter API access
		auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
		auth.set_access_token( ACCESS_KEY, ACCESS_SECRET )
		api = tweepy.API( auth )

		# begin keeping track of statistics during API calls
		start_time = time.time()
		tweet_count_total = 0
		chain = {}

		# get user's latest tweets
		for tweet in tweepy.Cursor( api.user_timeline, id=twitter_id, tweet_mode='extended' ).items():
			if tweet.full_text.startswith( ( "RT @", "https://t.co/" ) ) == False:
				# arrange individual words into Markov chains (collect data on user's typing style)
				words = tweet.full_text.split()
				for i in range( 0, len( words ) ):
					if words[i] not in chain:
							chain[words[i]] = []
					if i == len( words ) - 1:
						chain[words[i]].append(0)
					else:
						chain[words[i]].append( words[i + 1] )
			tweet_count_total += 1

		# display API fetch statistics
		elapsed_time = time.time() - start_time
		await ctx.send( "analyzed {} tweets from @{} in {}".format( tweet_count_total, acc_tag, elapsed_time ) )

def setup( bot ):
	bot.add_cog( Twitter( bot ) )