import discord
import traceback
import aiosqlite
import datetime
import asyncio
import sqlite3
import random
import sys
import os
from pathlib import Path
from discord.ext import commands
from information import config
from mutagen.mp3 import MP3
import re
import difflib
import requests
from discord.ext.commands import BucketType

HeadURL = f'https://splatoonwiki.org/wiki/Template:Gear/S2_Headgear?action=raw'
CheckerH = requests.get(HeadURL)
headgear_txt = CheckerH.text

ShirtURL = f'https://splatoonwiki.org/wiki/Template:Gear/S2_Clothing?action=raw'
CheckerSHT = requests.get(ShirtURL)
shirt_txt = CheckerSHT.text

ShoeURL = f'https://splatoonwiki.org/wiki/Template:Gear/S2_Shoes?action=raw'
CheckerSHO = requests.get(ShoeURL)
shoes_txt = CheckerSHO.text

maplist = ['hotel', 'wahoo', 'mall', 'skatepark', 'camp', 'arena', 'pumptrack', 'academy', 'dome', 'mart', 'manta', 'towers', 'fitness', 'pit', 'port', 'institute', 'canal', 'mainstage', 'reef', 'warehouse']
mapsgameview = {
    'mall': 'https://cdn.discordapp.com/attachments/441343994153402371/441345585581260810/mall-map.png',
    'skatepark': 'https://cdn.discordapp.com/attachments/441343994153402371/441345802162405396/skatepark-map.png',
    'camp': 'https://cdn.discordapp.com/attachments/441343994153402371/441345384980414504/camp-map.png',
    'arena': 'https://cdn.discordapp.com/attachments/441343994153402371/441345378026258432/arena-map.png',
    'pumptrack': 'https://cdn.discordapp.com/attachments/441343994153402371/441345706419159060/pumptrack-map.png',
    'academy': 'https://cdn.discordapp.com/attachments/441343994153402371/441345371344732162/academy-map.png',
    'dome': 'https://cdn.discordapp.com/attachments/441343994153402371/441345398477422592/dome-map.png',
    'mart': 'https://cdn.discordapp.com/attachments/441343994153402371/441345598088544256/mart-map.png',
    'manta': 'https://cdn.discordapp.com/attachments/441343994153402371/441345594557202442/manta-map.png',
    'towers': 'https://cdn.discordapp.com/attachments/441343994153402371/441345807677915146/towers-new-map.png',
    'fitness': 'https://cdn.discordapp.com/attachments/441343994153402371/441345566648172564/fitness-map.png',
    'pit': 'https://cdn.discordapp.com/attachments/441343994153402371/441345691483242508/pit-map.png',
    'port': 'https://cdn.discordapp.com/attachments/441343994153402371/441345702313066507/port-map.png',
    'institute': 'https://cdn.discordapp.com/attachments/441343994153402371/441345573270847488/institute-map.png',
    'canal': 'https://cdn.discordapp.com/attachments/441343994153402371/441345391754084352/canal-map.png',
    'mainstage': 'https://cdn.discordapp.com/attachments/441343994153402371/441345581000949770/mainstage-map.png',
    'reef': 'https://cdn.discordapp.com/attachments/441343994153402371/442534354384584714/reef-map.png',
    'warehouse': 'https://cdn.discordapp.com/attachments/441343994153402371/441345808210591744/warehouse-map.png',
    'wahoo': 'https://cdn.discordapp.com/attachments/455987115407441921/463405764695031809/world-map.png',
    'hotel': 'https://cdn.discordapp.com/attachments/455987115407441921/463406463373803523/hotel-map-pre.png',
}

mapsoverview = {
    'mall': 'https://cdn.discordapp.com/attachments/444297968049455125/444575753779150849/mall-overhead.png',
    'skatepark': 'https://cdn.discordapp.com/attachments/444297968049455125/444575782166200322/skatepark-overhead.png',
    'camp': 'https://cdn.discordapp.com/attachments/444297968049455125/444575812167925790/camp-overhead.png',
    'arena': 'https://cdn.discordapp.com/attachments/444297968049455125/444575841960198144/pumptrack-overhead.png',
    'pumptrack': 'https://cdn.discordapp.com/attachments/441343994153402371/441345706419159060/pumptrack-map.png',
    'academy': 'https://cdn.discordapp.com/attachments/444297968049455125/444575889255301120/academy-overhead.png',
    'dome': 'https://cdn.discordapp.com/attachments/444297968049455125/444575899090812938/dome-overhead.png',
    'mart': 'https://cdn.discordapp.com/attachments/444297968049455125/444575946444505098/mart-overhead.png',
    'manta': 'https://cdn.discordapp.com/attachments/444297968049455125/444575960315199489/manta_overhead.png',
    'towers': 'https://cdn.discordapp.com/attachments/444297968049455125/444575976047771648/towers-new-overhead.png',
    'fitness': 'https://cdn.discordapp.com/attachments/444297968049455125/444576010575282176/fitness-overhead.png',
    'pit': 'https://cdn.discordapp.com/attachments/444297968049455125/444576039130103827/pit-overhead.png',
    'port': 'https://cdn.discordapp.com/attachments/444297968049455125/444576063062802463/port-overhead.png',
    'institute': 'https://cdn.discordapp.com/attachments/444297968049455125/444576095916785665/institute-overhead.png',
    'canal': 'https://cdn.discordapp.com/attachments/444297968049455125/444576184576245807/canal-overhead.png',
    'mainstage': 'https://cdn.discordapp.com/attachments/444297968049455125/444576215697850378/mainstage-overhead.png',
    'reef': 'https://cdn.discordapp.com/attachments/444297968049455125/444576295607861248/reef-overhead.png',
    'warehouse': 'https://cdn.discordapp.com/attachments/444297968049455125/444576321784250369/warehouse-overhead.png',
    'wahoo': 'https://cdn.discordapp.com/attachments/455987115407441921/463405767412678686/world-overhead.png',
    'hotel': 'https://cdn.discordapp.com/attachments/455987115407441921/463406462450925578/hotel-overhead-pre.png',
}

class Utility:
    """Utility Module"""

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command(pass_context=True, name='suggestion')
    async def bot_private_suggestion(self, ctx, *, message):
	    user = self.bot.get_user(344289705627484163)
	    embed=discord.Embed(color=discord.Colour.dark_grey())
	    embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
	    embed.add_field(name=f'Suggestion from ({ctx.message.author.id} - {ctx.message.author.name})', value=f'{message}', inline=True)
	    await user.send(embed=embed)

    @commands.command(pass_context=True, name='reply')
    @commands.is_owner()
    async def bot_private_reply(self, ctx, user: discord.User, *, message):
	    userreply = self.bot.get_user(user.id)
	    embed=discord.Embed(color=discord.Colour.dark_grey())
	    embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
	    embed.add_field(name=f'Reply From VeeMOE', value=f'{message}', inline=True)
	    await userreply.send(embed=embed)

    @commands.group()
    async def utility(self, ctx):
        return

    @utility.command()
    async def callout(self, ctx, view, *, mapname):
        if mapname.lower() in maplist:
            if view.lower() == 'overview':
                embed=discord.Embed(title='Map Overview', color=discord.Colour.dark_grey())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url),
                embed.set_image(url=mapsoverview[mapname.lower()])
                await ctx.send(embed=embed)
            if view.lower() == 'gameview':
                embed=discord.Embed(title='Map Game View', color=discord.Colour.dark_grey())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url),
                embed.set_image(url=mapsgameview[mapname.lower()])
                await ctx.send(embed=embed)
            if not view.lower() == 'overview' and not view.lower() == 'gameview':
                embed=discord.Embed(description=f'{ctx.message.author.name} That is not a Valid View! ```VALID VIEW:\nGameView\nOverView```', color=discord.Colour.dark_grey())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url),
                await ctx.send(embed=embed)
        else:
            Cursor, VMP = 0, ''
            for item in maplist:
                VMP += '\n' + maplist[Cursor]
                Cursor += 1
            embed=discord.Embed(description=f'{ctx.message.author.name} That is not a Map Name! ```VALID MAPS:{VMP}```', color=discord.Colour.dark_grey())
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url),
            await ctx.send(embed=embed)

    @utility.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix):
        if ctx.message.author.bot == True:
            return
        else:
            try:
                prefixcheck = int(prefix)
            except:
                prefixcheck = prefix
            if not prefix.isalpha() and not type(prefixcheck) == int:
                conn = sqlite3.connect('splatoon-bot.db')
                cur = conn.cursor()
                cur.execute('SELECT P FROM Prefix WHERE ID=?', (ctx.message.guild.id,))
                CheckExist = cur.fetchone()
                if CheckExist:
	                cur.execute('UPDATE Prefix SET P=? WHERE ID=?', (prefix, ctx.message.guild.id,))
	                conn.commit()
	                cur.close()
	                self.bot.prefix_dict[ctx.message.guild.id] = prefix
                else:
	                cur.execute('INSERT Into Prefix(ID, P) VALUES(?, ?)', (ctx.message.guild.id, prefix))
	                conn.commit()
	                cur.close()
	                self.bot.prefix_dict[ctx.message.guild.id] = prefix
                embed=discord.Embed(color=discord.Colour.dark_grey())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                embed.add_field(name='Server Prefix Set!', value=f'{ctx.message.author.mention} has set the Guild Prefix to {prefix}', inline=True)
                await ctx.send(embed=embed)
                cur.close()
            else:
                embed=discord.Embed(color=discord.Colour.dark_grey())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                embed.add_field(name='Invalid Prefix', value=f'{ctx.message.author.mention} Prefixes Can Only Be Symbols, Example: !$@% Ect.', inline=True)
                await ctx.send(embed=embed)

    @utility.command(ignore_extra=False, case_insensitive=True)
    async def mem(self, ctx, memint):
        """Mem Cake Viewer"""
        if ctx.message.author.bot == True:
            return
        else:
            try:
                if int(memint) < 10:
                    try:
                        Query = f'OctCollectIcon_0{int(memint) - 1}'
                    except:
                        Query = f'OctCollectIcon_00'
                else:
                    Query = f'OctCollectIcon_{int(memint) - 1}'
                Search, NameSearch = self.bot.constant.Mem_Dict[Query], self.bot.constant.Mem_Name[Query]
                f = discord.File(f"{self.bot.directory}/images/Mem_Cake/{Query}.png", f"{Query}.png") 
                embed=discord.Embed(color=self.bot.config.color, )
                embed.add_field(name=f'{NameSearch}', value=f'{Search}', inline=True)
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.set_thumbnail(url=f"attachment://{Query}.png")
                await ctx.send(file=f, embed=embed)
            except:
                embed=discord.Embed(color=self.bot.config.color,description=f'*[SEARCHING_FOR_MEM]*\n*[MEM_NOT_FOUND]*')
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                await ctx.send(embed=embed) 

    @utility.command(name='rotation-add')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, type=BucketType.user)
    async def rotation_debug(self, ctx):
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        cur.execute('SELECT Channel FROM RotationChannel WHERE Channel=?', (ctx.message.channel.id,))
        Check = cur.fetchone()
        print(Check)
        if Check:
            cur.execute('DELETE FROM RotationChannel WHERE Channel=?', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='Rotation Channel Deleted!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is no longer a Rotation Channel!", inline=False)
            await ctx.send(embed=embed)
        if not Check:
            cur.execute('INSERT INTO RotationChannel(Channel) VALUES(?)', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='Rotation Channel Created!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is now a Rotation Channel!", inline=False)
            await ctx.send(embed=embed)
        cur.close()

    @utility.command(name='grizzco-add')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, type=BucketType.user)
    async def grizzco_debug(self, ctx):
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        cur.execute('SELECT Channel FROM GrizzChannel WHERE Channel=?', (ctx.message.channel.id,))
        Check = cur.fetchone()
        print(Check)
        if Check:
            cur.execute('DELETE FROM GrizzChannel WHERE Channel=?', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='Grizzco Channel Deleted!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is no longer a Grizzco Channel!", inline=False)
            await ctx.send(embed=embed)
        if not Check:
            cur.execute('INSERT INTO GrizzChannel(Channel) VALUES(?)', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='Grizzco Channel Created!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is now a Grizzco Channel!", inline=False)
            await ctx.send(embed=embed)
        cur.close()

    @utility.command(name='splatnet-add')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 60, type=BucketType.user)
    async def splatnet_debug(self, ctx):
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        cur.execute('SELECT Channel FROM SplatNetChannel WHERE Channel=?', (ctx.message.channel.id,))
        Check = cur.fetchone()
        print(Check)
        if Check:
            cur.execute('DELETE FROM SplatNetChannel WHERE Channel=?', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='SplatNet Channel Deleted!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is no longer a SplatNet2 Channel!", inline=False)
            await ctx.send(embed=embed)
        if not Check:
            cur.execute('INSERT INTO SplatNetChannel(Channel) VALUES(?)', (ctx.message.channel.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.dark_grey(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='SplatNet Channel Created!', value=f"{ctx.message.author.mention} the Channel {ctx.message.channel.mention} is now a SplatNet2 Channel!", inline=False)
            await ctx.send(embed=embed)
        cur.close()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def avatar(self, ctx, directory):
        if ctx.message.author.bot == True:
            return
        else:
            with open(f'/Users/shanehawkins/Desktop/Bot/bot/images/BotIcon/{directory}.png', 'rb') as f:
                await self.bot.user.edit(avatar=f.read())
            print('Avatar has successfully been set!')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def username(self, ctx, username):
        if ctx.message.author.bot == True:
            return
        else:
            await self.bot.user.edit(username=username)
            print('Username has successfully been set!')


def setup(bot):
    bot.add_cog(Utility(bot))