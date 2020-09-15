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

	""" tweet generator using unweighted Markov chain """
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

		try:
			chain = text_seqs.Markov_Chain()
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
			embed.set_author( name="@{}".format( embed_info['screen_name'] ), url="https://twitter.com/{}".format( embed_info['screen_name'] ), icon_url=embed_info['profile_image_url'] )
			embed.set_footer( text="analyzed {} tweets in {} seconds".format( tweet_count_total, elapsed_time ) )
			await ctx.send( embed=embed )

		except Exception as e:
			print( e )
			await ctx.send( "An error occurred while trying to analyze tweets from @{}".format( twitter_id ) )

def setup( bot ):
	bot.add_cog( Twitter( bot ) )