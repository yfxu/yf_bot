import os
import time
import discord
import tweepy

from .utils import arg_parse
from .utils import text_seqs
from discord.ext import commands
from dotenv import load_dotenv

# constants
TWEET_CHAR_LIMIT = 280
TWEET_FETCH_LIMIT = 500

# import authentication credentials
load_dotenv()
CONSUMER_KEY = os.getenv( 'CONSUMER_KEY' )
CONSUMER_SECRET = os.getenv( 'CONSUMER_SECRET' )
ACCESS_KEY = os.getenv( 'ACCESS_KEY' )
ACCESS_SECRET = os.getenv( 'ACCESS_SECRET' )

class Twitter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command( name='tweetgen', hidden=True, description="""Usage: tweetgen [Twitter ID] [N]
		> [Twitter ID] - Any user's Twitter ID (eg. @realDonaldTrump) case-insensitive
		> [N] - n-gram size (defaults to 1)""" )

	async def _tweetgen( self, ctx ):
		""" tweet generator using ngrams with configurable size """
		args = arg_parse.parse( ctx.message.content )
		
		try:
			twitter_id = args[0].strip( '@' )
		except Exception as e:
			print( "tweetgen load args[0]: {}".format( e ) )
			await ctx.send( "No Twitter id was provided" )
			return

		try:
			n = int( args[1] )
		except Exception as e:
			print( "tweetgen load args[1]: {}".format( e ) )
			n = 1

		# begin keeping track of statistics during API calls
		start_time = time.time()
		tweet_count_total = 0
		chain = {}

		# authentic bot for Twitter API access
		auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
		auth.set_access_token( ACCESS_KEY, ACCESS_SECRET )
		api = tweepy.API( auth )

		try:
			chain = text_seqs.Ngram( n )
			generated_tweet = "https://"

			# fetch user's latest tweets and feed them into a Markov chain
			for tweet in tweepy.Cursor( api.user_timeline, id=twitter_id, tweet_mode='extended' ).items( TWEET_FETCH_LIMIT ):
				if tweet.full_text.startswith( ( "RT @", "https://t.co/" ) ) == False:
					chain.feed( tweet.full_text )
				tweet_count_total += 1

			# generate the tweet given the Markov chain / exclude posts that begin with a link
			while( generated_tweet.startswith( "https://" ) ):
				generated_tweet = chain.generate( TWEET_CHAR_LIMIT )

			# display API fetch statistics
			elapsed_time = round( time.time() - start_time, 3 )

			# generate embed
			embed_info = api.get_user( twitter_id )._json
			embed = discord.Embed( description=generated_tweet, color=0x1da1f2 )
			embed.set_author( name="{}  @{}".format( embed_info['name'], embed_info['screen_name'] ), url="https://twitter.com/{}".format( embed_info['screen_name'] ), icon_url=embed_info['profile_image_url'] )
			embed.set_footer( text="analyzed {} tweets in {} seconds  |  created using n-grams ( N = {} )".format( tweet_count_total, elapsed_time, n ) )
			await ctx.send( embed=embed )

		except Exception as e:
			print( "what the fuck: {}".format( e ) )
			await ctx.send( "An error occurred while trying to analyze tweets from @{}".format( twitter_id ) )

def setup( bot ):
	bot.add_cog( Twitter( bot ) )