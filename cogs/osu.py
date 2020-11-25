import discord
import json
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
from .utils import arg_parse
from .utils import time_utils

load_dotenv()

class Osu( commands.Cog ):
	"""osu! cog"""
	def __init__( self, bot ):
		self.bot = bot
		self.api_key = os.getenv( 'OSU_TOKEN' )
		self.base_url = "https://osu.ppy.sh"


	# ------------------- common osu functions ------------------- #

	# Return dictionary containing mode name and id
	def get_mode_id( self, osu_mode ):
		osu_mode = str( osu_mode )

		if osu_mode.lower() == "taiko" or osu_mode.lower() == "t" or osu_mode == "1":
			return { "name": "osu!taiko", "id": 1 }
		elif osu_mode.lower() == "catch" or osu_mode.lower() == "c" or osu_mode.lower() == "ctb" or osu_mode == "2":
			return { "name": "osu!catch", "id": 2 }
		elif osu_mode.lower() == "mania" or osu_mode.lower() == "m" or osu_mode == "3":
			return { "name": "osu!mania", "id": 3 }
		else: 
			return { "name": "osu!std", "id": 0 }


	# Return mod name from mod id
	def get_mod_name( self, mod_id ):
		mods = {
			"0": "NM",
			"1": "NF",
			"2": "EZ",
			"4": "TD",
			"8": "HD",
			"16": "HR",
			"32": "SD",
			"64": "TD",
			"128": "RX",
			"256": "HT",
			"512": "NC",
			"1024": "FL",
			"2048": "AUTO",
			"4096": "SO",
			"8192": "AP",
			"16384": "PF",
			"32768": "K4",
			"65536": "K5",
			"131072": "K6",
			"262144": "K7",
			"524288": "K8",
			"1048576": "FI",
			"2097152": "RANDOM",
			"4194304": "CINEMA",
			"8388608": "TARGET",
			"16777216": "K9",
			"33554432": "KC",
			"67108864": "K1",
			"134217728": "K2",
			"268435456": "K3",
			"536870912": "V2",
			"1073741824": "MI"
		}
		try:
			return mods[mod_id]
		except:
			return "MOD NOT FOUND"

	# Fetch get_user from osu! api v1
	def get_user_info( self, osu_user_id, osu_mode_id=0 ):
		return requests.get( self.base_url + "/api/get_user", params={
			'k': self.api_key, 
			'u': osu_user_id, 
			'm': osu_mode_id,
			'type': 'string'} ).json()[0]


	# Fetch get_user_best from osu! api v1
	def get_user_best_info( self, osu_user_id, osu_mode_id=0, osu_limit=100 ):
		return requests.get( self.base_url + "/api/get_user_best", params={
			'k': self.api_key, 
			'u': osu_user_id, 
			'm': osu_mode_id,
			'limit': osu_limit,
			'type': 'string'} ).json()


	# Fetch get_user_best from osu! api v1
	def get_beatmap_info( self, since=None, s=None, b=None, u=None, u_type=None, m=None, a=None, h=None, limit=None, mods=None ):
		return requests.get( self.base_url + "/api/get_beatmaps", params={
			'k': self.api_key, 
			'since': since,
			's': s,
			'b': b,
			'u': u,
			'type': u_type,
			'm': m,
			'a': a,
			'h': h,
			'limit': limit,
			'mods': mods } ).json()


	# ------------------- osu! discord commands ------------------- #

	@commands.command( name="osu" )
	async def _get_osu_user( self, ctx ):
		""" Output embed with basic osu player stats """
		args = arg_parse.parse( ctx.message.content )
		if len( args ) == 0:
			await ctx.send("No user was provided")
			return

		try:
			osu_user_id = args[0]
			osu_mode = self.get_mode_id( args[1] )
		except:
			osu_user_id = args[0]
			osu_mode = self.get_mode_id( 0 )

		r = self.get_user_info( osu_user_id, osu_mode['id'] )

		embed = discord.Embed(
			title = ":flag_{}:  {}  (#{})  ({}#{})".format(r['country'].lower(), r['username'], r['pp_rank'], r['country'], r['pp_country_rank']), 
			url = self.base_url + "/u/" + r['user_id'],
			colour = discord.Colour( 0xfcba03 ),
			description = """**Total PP:**  {}
**Accuracy:**  {}%
**Playcount:**  {}
**Join date:**  {}
""".format( r['pp_raw'], "{:.2f}".format( float( r['accuracy'] ) ), r['playcount'], r['join_date'])
		)
		embed.set_thumbnail( url = "https://a.ppy.sh/{}".format( r['user_id'] ) )
		embed.set_footer( text = "{} profile for {}".format( osu_mode['name'], r['username'] ) )

		await ctx.send( embed = embed )


	@commands.command(name="mapper")
	async def _get_osu_mapper(self, ctx):
		"""Get mapper stats"""
		args = arg_parse.parse( ctx.message.content )
		if len( args ) == 0:
			await ctx.send("No user was provided")
			return

		user_id = args[0]

		sets = []
		maps = self.get_beatmap_info(u=user_id)
		user = self.get_user_info(user_id)

		for m in maps:
			if m['beatmapset_id'] not in [ s['beatmapset_id'] for s in sets ]:
				sets.append(m.copy())
			else:
				for s in sets:
					if s['beatmapset_id'] == m['beatmapset_id']:
						s['playcount'] = str(int(s['playcount']) + int(m['playcount']))

		stats = {
			'total_sets'     : len(sets),
			'total_diffs'    : len(maps),
			'total_plays'    : sum([ int(x['playcount']) for x in maps ]),
			'total_favs'     : sum([ int(x['favourite_count']) for x in sets ]),
			'total_drain'    : sum([ int(x['hit_length']) for x in maps ]),
			'most_play_diff' : max(maps, key=lambda x:int(x['playcount'])), 
			'most_play_set'  : max(sets, key=lambda x:int(x['playcount'])), 
			'most_fav_set'   : max(sets, key=lambda x:int(x['favourite_count'])) 
		}

		embed = discord.Embed(
			title=f":flag_{user['country'].lower()}: {user['username']}'s mapper profile",
			url=self.base_url + f"/u/{user['user_id']}",
			description="**beatmap sets:** {:,}\n**beatmaps:** {:,}\n**playcount:** {:,}\n**favourites:** {:,}\n**drain time mapped:** {}".format(
				stats['total_sets'],
				stats['total_diffs'],
				stats['total_plays'],
				stats['total_favs'],
				time_utils.format_str(stats['total_drain'])
				)
			)
		embed.add_field(name="most favourited mapset", value=f"♥ {int(stats['most_fav_set']['favourite_count']):,} | {stats['most_fav_set']['artist']} - {stats['most_fav_set']['title']}", inline=False)
		embed.add_field(name="most played mapset", value=f"► {int(stats['most_play_set']['playcount']):,} | {stats['most_play_set']['artist']} - {stats['most_play_set']['title']}", inline=False)
		embed.add_field(name="most played difficulty", value=f"► {int(stats['most_play_diff']['playcount']):,} | {stats['most_play_diff']['artist']} - {stats['most_play_diff']['title']} [{stats['most_play_diff']['version']}]", inline=False)
		embed.set_thumbnail(url="https://a.ppy.sh/{}".format(user['user_id']))

		await ctx.send( embed=embed )

	@commands.command( name="onemiss" )
	async def _get_onemiss( self, ctx ):
		""" Output 1x miss statistics """
		args = arg_parse.parse( ctx.message.content )
		if len( args ) == 0:
			await ctx.send( "No user was provided" )
			return

		osu_user_id = args[0]

		top_plays = self.get_user_best_info( osu_user_id, osu_user_id )
		onemiss_plays = [play for play in top_plays if play['countmiss'] == '1']
		onemiss_cnt = len( onemiss_plays )

		await ctx.send( "{} has {} 1x misses in their top 100 plays!".format( osu_user_id, onemiss_cnt ) )
	
def setup( bot ):
	bot.add_cog( Osu( bot ) )