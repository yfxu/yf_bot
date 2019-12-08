# yf_bot.py
import discord
import os
import random
import sqlite3
import requests
from dotenv import load_dotenv
from datetime import datetime

command_prefix = "y."
bot_folder = r"C:\\Users\\yifei\\Documents\\yf_bot"

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
osu_token = os.getenv('OSU_TOKEN')

client = discord.Client()


# Get stats about a particular osu user
def get_osu_user(osu_user_id, osu_mode = "std"):
	if osu_mode.lower() == "taiko" or osu_mode.lower() == "t":
		osu_mode = "osu!taiko"
		osu_mode_id = 1
	elif osu_mode.lower() == "catch" or osu_mode.lower() == "c" or osu_mode.lower() == "ctb":
		osu_mode = "osu!catch"
		osu_mode_id = 2
	elif osu_mode.lower() == "mania" or osu_mode.lower() == "m":
		osu_mode = "osu!mania"
		osu_mode_id = 3
	else: 
		osu_mode = "osu!std"
		osu_mode_id = 0

	r = requests.get("https://osu.ppy.sh/api/get_user", params={'k': osu_token, 'u': osu_user_id, 'm': osu_mode_id}).json()[0]
	
	embed = discord.Embed(
		title = ":flag_{}:  {}  (#{})  ({}#{})".format(r['country'].lower(), r['username'], r['pp_rank'], r['country'], r['pp_country_rank']), 
		colour = discord.Colour(0xfcba03),
		description = """
		**Total PP:**  {}
		**Accuracy:**  {}%
		**Playcount:**  {}
		**Join date:**  {}
		""".format(r['pp_raw'], "{:.2f}".format(float(r['accuracy'])), r['playcount'], r['join_date'])
	)
	embed.set_thumbnail(url = "https://a.ppy.sh/{}".format(r['user_id']))
	embed.set_footer(text = "{} profile for {}".format(osu_mode, r['username']))

	return embed


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	print("[{}]".format(datetime.now()), "| Author:", message.author, "| Message:", message.content)

	# .roll
	# Generates a random number
	if str(message.content).split()[0] == command_prefix + "roll":
		msg_author = message.author

		try:
			roll_val = random.randrange(1, int(message.content.split()[1]) + 1, 1)
		except:
			roll_val = random.randrange(1, 7, 1)

		send_msg = ":game_die: {} rolled a {}".format(msg_author.mention, roll_val)

		await message.channel.send(send_msg)

	# track "xd" case-insensitive
	if "xd" in message.content.lower():
		xd_count = message.content.lower().count("xd")
		discord_server = "{}_{}".format(message.guild.name, message.guild.id)
		
		# Create a separate db file for each server
		conn = sqlite3.connect("{}\{}.db".format(bot_folder, discord_server))
		c = conn.cursor()
		c.execute("CREATE TABLE if not exists XD_TABLE( rowid INTEGER DEFAULT 0 PRIMARY KEY )")
		try:
			c.execute("INSERT INTO XD_TABLE VALUES(0)")
		except:
			pass

		# Format user's Discord id into valid column name
		# note: 'id' IS NOT the same as Discord tag
		user_column = "_{}".format(message.author.id)

		try:
			c.execute("ALTER TABLE XD_TABLE ADD COLUMN {} INTEGER DEFAULT 0".format(user_column))
		except:
			pass

		try:
			c.execute("UPDATE XD_TABLE SET {} = {} + {}".format(user_column, user_column, xd_count))
		except Exception as e:
			await message.channel.send(e)
			print(e)

		conn.commit()
		conn.close()

	# .xd
	# "xd" leaderboard
	if message.content == command_prefix + "xd":
		try:
			discord_server = "{}_{}".format(message.guild.name, message.guild.id)
			conn = sqlite3.connect("{}\{}.db".format(bot_folder, discord_server))
			conn.row_factory = sqlite3.Row
			c = conn.cursor()

			c.execute("SELECT * FROM XD_TABLE")
			xd_data = c.fetchall()
			xd_keys = c.description
			xd_msg = "'xd' counter\n------------\n"

			conn.close()

			#print("xd_data: {}".format(xd_data))
			#print("xd_keys: {}".format(xd_keys))

			for i in range(1, len(xd_keys)):
				xd_user = client.get_user(int(xd_keys[i][0].replace("_", "")))
				xd_count = xd_data[0][i]
				xd_msg += "{}: {}\n".format(xd_user, xd_count)

			await message.channel.send("```{}```".format(xd_msg))
		except Exception as e:
			await message.channel.send(e)

	if message.content.startswith(command_prefix + "osu"):
		try:
			await message.channel.send(embed = get_osu_user(message.content.split()[1], message.content.split()[2]))
		except:
			await message.channel.send(embed = get_osu_user(message.content.split()[1]))

		#try:
		#	await message.channel.send(embed = get_osu_user(message.content.split()[1], osu_mode))
		#except Exception as e:
		#	await message.channel.send("```{}```".format(e))
		#	#await message.channel.send("`User not found`")

client.run(token)