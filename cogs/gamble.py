import discord
import random
from .utils import arg_parse
from .utils import markdown
from discord.ext import commands

class Gamble(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='roll', hidden=True)
	async def _roll(self, ctx):
		roll_max = 6
		roll_count = 1
		args = arg_parse.parse(ctx.message.content)

		try:
			roll_max = int(args[0])
			roll_count = int(args[1])
		except:
			pass

		roll_vals = [str(random.randrange(1, roll_max + 1, 1)) for i in range(0,roll_count)]
		roll_sum = markdown.bold(sum([int(i) for i in roll_vals]))
		roll_list = ', '.join(roll_vals) + " " if len(roll_vals) > 1 else ""
		send_msg = ":game_die: <@{}> rolled {} >  {}".format(ctx.author.id, roll_list, roll_sum)

		await ctx.send(send_msg)

def setup(bot):
	bot.add_cog(Gamble(bot))