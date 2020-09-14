import os
import time
import random
import discord
import tweepy

from .utils import arg_parse
from discord.ext import commands
from dotenv import load_dotenv

# constants
TWEET_CHAR_LIMIT = 280
TWEET_FETCH_LIMIT = 250

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
		try:
			twitter_id = arg_parse.parse( ctx.message.content )[0].strip( '@' )
		except:
			await ctx.send( "No Twitter id was provided" )
			return

		# begin keeping track of statistics during API calls
		start_time = time.time()
		tweet_count_total = 0
		chain = {}

		# authentic bot for Twitter API access
		auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
		auth.set_access_token( ACCESS_KEY, ACCESS_SECRET )
		api = tweepy.API( auth )

		# get user's latest tweets
		try:
			for tweet in tweepy.Cursor( api.user_timeline, id=twitter_id, tweet_mode='extended' ).items( TWEET_FETCH_LIMIT ):
				if tweet.full_text.startswith( ( "RT @", "https://t.co/" ) ) == False:
					# arrange individual words into Markov chains (collect data on user's typing style)
					words = tweet.full_text.split()
					for i in range( 0, len( words ) ):
						if words[i] not in chain:
								chain[words[i]] = set()
						# end-of-tweet character
						if i == len( words ) - 1:
							chain[words[i]].add(0)
						else:
							chain[words[i]].add( words[i + 1] )
				tweet_count_total += 1

			# generate the tweet given the Markov chain
			last_word = random.choice( list( chain ) )
			generated_tweet = last_word
			while len( generated_tweet ) < TWEET_CHAR_LIMIT:
				last_word = random.choice( tuple( chain[last_word] ) )
				# special end-tweet character
				if last_word == 0:
					break
				generated_tweet += " " + last_word

			generated_tweet = generated_tweet[:280]

			# display API fetch statistics
			elapsed_time = round( time.time() - start_time, 3 )
			await ctx.send( "@{}: {}".format( twitter_id, generated_tweet ) )
			await ctx.send( "analyzed {} tweets from @{} in {}s".format( tweet_count_total, twitter_id, elapsed_time ) )
		except:
			await ctx.send( "An error occurred while trying to analyze tweets from @{}".format( twitter_id ) )

def setup( bot ):
	bot.add_cog( Twitter( bot ) )