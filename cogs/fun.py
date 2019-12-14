import codecs
import discord
import os
import random
import subprocess
from .utils import arg_parse
from .utils import markdown
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# ---------------------- Generic functions ---------------------- #

	""" Spongebob mock text, stolen from https://github.com/nkrim/spongemock/blob/master/src/spongemock.py#L9 """  
	def spongemock(self, text, diversity_bias=0.5, random_seed=None):
		# Error handling
		if diversity_bias < 0 or diversity_bias > 1:
			raise ValueError('diversity_bias must be between the inclusive range [0,1]')
		# Seed the random number generator
		random.seed(random_seed)
		# Mock the text
		out = ''
		last_was_upper = True
		swap_chance = 0.5
		for c in text:
			if c.isalpha():
				if random.random() < swap_chance:
					last_was_upper = not last_was_upper
					swap_chance = 0.5
				c = c.upper() if last_was_upper else c.lower()
				swap_chance += (1-swap_chance)*diversity_bias
			out += c
		return out


	# ---------------------- Commands ---------------------- #

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

	@commands.command(name='font', hidden=True)
	async def _font(self, ctx):
		try:
			args = ctx.message.content.split(' ', 2)
			font = args[1].lower()
			text = args[2]
			normal_font = u' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
			fonts = {
				"vape": u'　０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［\\］＾＿‘｛｜｝～',
				"old": u' 0123456789𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"old_bold": u' 0123456789𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"cursive": u' 𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵❢"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"cursive_bold": u' 0123456789𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"block": u' 0123456789🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"racist": u'　0123456789卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"art_deco": u' 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"serif": u' 𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~',
				"slant": u' 0123456789𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
			}

			if font == "spongebob":
				await ctx.send(self.spongemock(text))
			else:
				font_map = dict((ord(x[0]), x[1]) for x in zip(normal_font, fonts[font]))
				await ctx.send(text.translate(font_map))

		except Exception as e:
			print(e)
			await ctx.send(markdown.code_block("""Oh no invalid input!!! Your command must look like:
{}font [font_name] [text]
-----------------------------------------------
Available fonts: 
    vape, old, old_bold, cursive, cursive_bold,
    block, racist, art_deco, serif, slant, spongebob""".format(self.bot.command_prefix)))
		
def setup(bot):
	bot.add_cog(Fun(bot))