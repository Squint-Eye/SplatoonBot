import discord, traceback, aiosqlite, datetime, asyncio, sqlite3, random, aiohttp, sys, os, psutil
from pathlib import Path
from discord.ext import commands
from information import config, constant

prefix_dict = {}

#Main Directory Grabber
directory = os.path.dirname(__file__)

conn = sqlite3.connect('splatoon-bot.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Prefix(ID, P)')
cur.execute('Select ID FROM Prefix')
ID = cur.fetchall()
cur.execute('Select P FROM Prefix')
Prefix = cur.fetchall()
C = 0
for item in ID:
	prefix_dict[ID[C][0]] = Prefix[C][0]
	C += 1
cur.close()

async def get_prefix(bot, message):
	try:
		return bot.prefix_dict.get(message.guild.id, config.prefix)
	except:
		return config.prefix

bot = commands.AutoShardedBot(command_prefix=get_prefix)
bot.prefix_dict = prefix_dict
bot.config = config
bot.constant = constant
bot.directory = directory
bot.remove_command('help')

async def load_cog():
	cog_dir = Path('./cogs')
	cog_dir.mkdir(exist_ok=True)
	for ex in cog_dir.iterdir():
		if ex.suffix == '.py':
			path = '.'.join(ex.with_suffix('').parts)
			bot.load_extension(path)

@bot.event
async def on_command_completion(ctx):
	try:
		Prefix = bot.prefix_dict.get(ctx.message.guild.id, ".")
		UsedIn = ctx.message.guild.name
	except:
		Prefix = '.'
		UsedIn = 'DM Channel'
	print(' '.join([f'{ctx.message.author.id} ({ctx.message.author}) - {UsedIn}) - {Prefix}{ctx.command} @', '{:%Y-%b-%d %H:%M}'.format(datetime.datetime.now())]))

@bot.event
async def on_ready():
	conn = sqlite3.connect('splatoon-bot.db')
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS Profile(ID, User, IGN, FC, Level, RM, TC, SZ, CB, Mem, Gender, Banner, Title)')
	cur.execute('CREATE TABLE IF NOT EXISTS Splatoon2(SplatNet2)')
	cur.execute('CREATE TABLE IF NOT EXISTS SplatNetChannel(Channel)')
	cur.execute('CREATE TABLE IF NOT EXISTS RotationChannel(Channel)')
	cur.execute('CREATE TABLE IF NOT EXISTS GrizzChannel(Channel)')
	cur.close()
	await load_cog()
	print('-' * 9 + f'{bot.config.name} is Online' + '-' * 9 + f'\nhttps://discordapp.com/oauth2/authorize?client_id={bot.config.uid}&scope=bot&permissions=2146958591')

@bot.command(pass_context=True, aliases=['discord'])
async def invite(ctx):
	f"""Displays Bot Links"""
	if ctx.invoked_with == 'discord':
		embed=discord.Embed(color=bot.config.color, title=f'{ctx.message.author.name} this is my Official Discord', url=f"https://discord.gg/ZCwQPwn")
	else:
		embed=discord.Embed(color=bot.config.color, title=f'{ctx.message.author.name} this is my invite', url=f"https://discordapp.com/oauth2/authorize?client_id={bot.config.uid}&scope=bot&permissions=8")
	embed.set_author(name=f"{bot.config.name}", icon_url=bot.config.url)
	embed.set_footer(text="Invite Generated at {:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now()))
	await ctx.send(embed=embed)

bot.run(bot.config.token)