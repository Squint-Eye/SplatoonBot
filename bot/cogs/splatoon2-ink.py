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
from datetime import datetime, timedelta
from discord.ext.commands import BucketType
import json
import requests

gamemode_list = ['turf war', 'ranked battle', 'league battle', 'turf', 'ranked', 'league',]
gamemode_converter = {'turf war': 'regular', 'ranked battle': 'gachi', 'league battle': 'league', 'turf': 'regular', 'ranked': 'gachi', 'league': 'league',}
gamemode_conv_name = {'turf war': 'Turf War', 'ranked battle': 'Ranked', 'league battle': 'League', 'turf': 'Turf War', 'ranked': 'Ranked', 'league': 'League', }

class Splatoon2_Ink:
    """Gamemode/Item Statistics"""

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.splatnet_loop())
        self.bg_task = self.bot.loop.create_task(self.grizzco_loop())
        self.bg_task = self.bot.loop.create_task(self.rotation_loop())
        SplatURL = 'https://splatoon2.ink/data/merchandises.json'
        SplatNet2 = requests.get(SplatURL)
        splat_file = SplatNet2.json()
        GrizzURL = 'https://splatoon2.ink/data/coop-schedules.json'
        GrizzCo = requests.get(GrizzURL)
        grizz_file = GrizzCo.json()
        GameURL = 'https://splatoon2.ink/data/schedules.json'
        GameMode = requests.get(GameURL)
        game_file = GameMode.json()
        self.LastItem = splat_file['merchandises'][5]['gear']['name']
        self.LastGrizzMap = grizz_file['details'][0]['stage']['name']
        self.LastRotationMap = game_file['league'][0]['stage_a']['name']

    async def rotation_check(self):
        GameURL = 'https://splatoon2.ink/data/schedules.json'
        GameMode = requests.get(GameURL)
        game_file = GameMode.json()
        Map1R, Map2R = game_file['regular'][0]['stage_a']['name'], game_file['regular'][0]['stage_b']['name']
        GameModeR = game_file['regular'][0]['rule']['name']
        StartTimeR, EndTimeR = datetime.fromtimestamp(game_file['regular'][0]['start_time']).ctime(), datetime.fromtimestamp(game_file['regular'][0]['end_time']).ctime()
        Map1S, Map2S = game_file['gachi'][0]['stage_a']['name'], game_file['gachi'][0]['stage_b']['name']
        GameModeS = game_file['gachi'][0]['rule']['name']
        StartTimeS, EndTimeS = datetime.fromtimestamp(game_file['gachi'][0]['start_time']).ctime(), datetime.fromtimestamp(game_file['gachi'][0]['end_time']).ctime()
        Map1L, Map2L = game_file['league'][0]['stage_a']['name'], game_file['league'][0]['stage_b']['name']
        GameModeL = game_file['league'][0]['rule']['name']
        StartTimeL, EndTimeL = datetime.fromtimestamp(game_file['league'][0]['start_time']).ctime(), datetime.fromtimestamp(game_file['league'][0]['end_time']).ctime()
        if self.LastRotationMap != game_file['league'][0]['stage_a']['name']:
            print('Sending Rotations...')
            self.LastRotationMap = game_file['league'][0]['stage_a']['name']
            conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
            cur = conn.cursor()
            cur.execute('SELECT Channel FROM RotationChannel')
            RotationSend = cur.fetchall()
            Cursor = 0
            for item in RotationSend:
                try:
                    channel = self.bot.get_channel(RotationSend[Cursor][0])
                    f = discord.File(f"{self.bot.directory}/images/gamemode_icon/Turf.png", f"Turf.png") 
                    embed=discord.Embed(color=discord.Colour.red())
                    embed.add_field(name=f"Current Turf War Rotation Active Through", value=f'`{StartTimeR} - {EndTimeR}`', inline=False)
                    embed.add_field(name=f"Current Turf War Gamemode", value=f'`{GameModeR}`', inline=True)
                    embed.add_field(name=f"Current Turf War Maps", value=f'`{Map1R}`\n`{Map2R}`', inline=True)
                    embed.set_thumbnail(url=f"attachment://Turf.png")
                    embed.set_footer(text='Information Grabbed From splatoon2.ink')
                    await channel.send(file=f, embed=embed)
                    f = discord.File(f"{self.bot.directory}/images/gamemode_icon/Ranked.png", f"Ranked.png") 
                    embed=discord.Embed(color=discord.Colour.red())
                    embed.add_field(name=f"Current Ranked Battle Rotation Active Through", value=f'`{StartTimeS} - {EndTimeS}`', inline=False)
                    embed.add_field(name=f"Current Ranked Battle Gamemode", value=f'`{GameModeS}`', inline=True)
                    embed.add_field(name=f"Current Ranked Battle Maps", value=f'`{Map1S}`\n`{Map2S}`', inline=True)
                    embed.set_thumbnail(url=f"attachment://Ranked.png")
                    embed.set_footer(text='Information Grabbed From splatoon2.ink')
                    await channel.send(file=f, embed=embed)
                    f = discord.File(f"{self.bot.directory}/images/gamemode_icon/League.png", f"League.png") 
                    embed=discord.Embed(color=discord.Colour.red())
                    embed.add_field(name=f"Current League Battle Rotation Active Through", value=f'`{StartTimeL} - {EndTimeL}`', inline=False)
                    embed.add_field(name=f"Current League Battle Gamemode", value=f'`{GameModeL}`', inline=True)
                    embed.add_field(name=f"Current League Battle Maps", value=f'`{Map1L}`\n`{Map2L}`', inline=True)
                    embed.set_thumbnail(url=f"attachment://League.png")
                    embed.set_footer(text='Information Grabbed From splatoon2.ink')
                    await channel.send(file=f, embed=embed)
                except:
                    pass
                Cursor += 1



    async def grizzco_check(self):
        GrizzURL = 'https://splatoon2.ink/data/coop-schedules.json'
        GrizzCo = requests.get(GrizzURL)
        grizz_file = GrizzCo.json()
        if self.LastGrizzMap != grizz_file['details'][0]['stage']['name']:
            self.LastGrizzMap = grizz_file['details'][0]['stage']['name']
            GrizzTime, GrizzEnd = datetime.fromtimestamp(grizz_file['details'][0]['start_time']).ctime(), datetime.fromtimestamp(grizz_file['details'][0]['end_time']).ctime()
            GrizzMap = grizz_file['details'][0]['stage']['name']
            GrizzIcon = grizz_file['details'][0]['stage']['image']
            try:
                GrizzWep1 = grizz_file['details'][0]['weapons'][0]['weapon']['name']
                GrizzSub1 = grizz_file['details'][0]['weapons'][0]['weapon']['sub']['name']
                GrizzSpecial1 = grizz_file['details'][0]['weapons'][0]['weapon']['special']['name']
            except:
                GrizzWep1 = 'Random'
                GrizzSub1 = 'Unknown'
                GrizzSpecial1 = 'Unknown'
            try:
                GrizzWep2 = grizz_file['details'][0]['weapons'][1]['weapon']['name']
                GrizzSub2 = grizz_file['details'][0]['weapons'][1]['weapon']['sub']['name']
                GrizzSpecial2 = grizz_file['details'][0]['weapons'][1]['weapon']['special']['name']
            except:
                GrizzWep2 = 'Random'
                GrizzSub2 = 'Unknown'
                GrizzSpecial2 = 'Unknown'
            try:
                GrizzWep3 = grizz_file['details'][0]['weapons'][2]['weapon']['name']
                GrizzSub3 = grizz_file['details'][0]['weapons'][2]['weapon']['sub']['name']
                GrizzSpecial3 = grizz_file['details'][0]['weapons'][2]['weapon']['special']['name']
            except:
                GrizzWep3 = 'Random'
                GrizzSub3 = 'Unknown'
                GrizzSpecial3 = 'Unknown'
            try:
                GrizzWep4 = grizz_file['details'][0]['weapons'][3]['weapon']['name']
                GrizzSub4 = grizz_file['details'][0]['weapons'][3]['weapon']['sub']['name']
                GrizzSpecial4 = grizz_file['details'][0]['weapons'][3]['weapon']['special']['name']
            except:
                GrizzWep4 = 'Random'
                GrizzSub4 = 'Unknown'
                GrizzSpecial4 = 'Unknown'
            conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
            cur = conn.cursor()
            cur.execute('SELECT Channel FROM GrizzChannel')
            GrizzSend = cur.fetchall()
            Cursor = 0
            for item in GrizzSend:
                print('Sending Salmon Run Information')
                try:
                    channel = self.bot.get_channel(GrizzSend[Cursor][0])
                    if channel != None:
                        embed=discord.Embed(color=discord.Colour.orange())
                        embed.add_field(name=f"Latest Salmon Run Information ({GrizzMap})", value=f'`{GrizzTime} - {GrizzEnd} - UTC/GMT`', inline=True)
                        embed.add_field(name=f"Weapons", value=f'`{GrizzWep1} ({GrizzSub1}) ({GrizzSpecial1})`\n`{GrizzWep2} ({GrizzSub2}) ({GrizzSpecial2})`\n`{GrizzWep3} ({GrizzSub3}) ({GrizzSpecial3})`\n`{GrizzWep4} ({GrizzSub4}) ({GrizzSpecial4})`', inline=False)
                        embed.set_image(url=f'https://splatoon2.ink/assets/splatnet{GrizzIcon}')
                        embed.set_footer(text='Information Grabbed From splatoon2.ink')
                        await channel.send(embed=embed)
                except:
                    pass
                Cursor += 1

    async def splatnet_check(self):
        SplatURL = 'https://splatoon2.ink/data/merchandises.json'
        SplatNet2 = requests.get(SplatURL)
        splat_file = SplatNet2.json()
        if self.LastItem != splat_file['merchandises'][5]['gear']['name']:
            self.LastItem = splat_file['merchandises'][5]['gear']['name']
            conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
            cur = conn.cursor()
            cur.execute('SELECT Channel FROM SplatNetChannel')
            Channel = cur.fetchall()
            Cursor = 0
            for item in Channel:
                print('Sending SplatNet2 Information...')
                try:
                    channel = self.bot.get_channel(Channel[Cursor][0])
                    if channel != None:
                        S1Name, S1Brand, S1Cost, S1Skill, S1Ability, S1Icon, S1End = splat_file['merchandises'][5]['gear']['name'], splat_file['merchandises'][5]['gear']['brand']['name'], splat_file['merchandises'][5]['price'], splat_file['merchandises'][5]['skill']['name'], splat_file['merchandises'][5]['gear']['brand']['frequent_skill']['name'], splat_file['merchandises'][5]['gear']['image'], datetime.fromtimestamp(splat_file['merchandises'][5]['end_time']).ctime()
                        embed=discord.Embed(color=discord.Colour.orange(), title=f'{S1Name} ({S1Brand})')
                        embed.add_field(name=f'Gear Price', value=f'<:Coin:460630467364913152> `{S1Cost}`', inline=True)
                        embed.add_field(name=f'Sale Ends At', value=f'`{S1End}`', inline=True)
                        embed.add_field(name=f'Main Ability', value=f'`{S1Skill}`', inline=True)
                        embed.add_field(name=f'Common Ability ({S1Brand})', value=f'`{S1Ability}`', inline=True)
                        embed.set_thumbnail(url=f'https://splatoon2.ink/assets/splatnet{S1Icon}')
                        embed.set_footer(text='Information Grabbed From splatoon2.ink')
                        await channel.send(embed=embed)
                except:
                    pass
                Cursor += 1

    async def auto_splatnet_check(self):
        SplatURL = 'https://splatoon2.ink/data/merchandises.json'
        SplatNet2 = requests.get(SplatURL)
        splat_file = SplatNet2.json()
        if self.LastItem != splat_file['merchandises'][5]['gear']['name']:
            self.LastItem = splat_file['merchandises'][5]['gear']['name']
            conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
            cur = conn.cursor()
            cur.execute('SELECT ID FROM AUTODM WHERE Item=?', (splat_file['merchandises'][5]['gear']['name'],))
            USERDM = cur.fetchall()
            Cursor = 0
            for item in USERDM:
                print('DMIng Users SplatNet2 Information...')
                try:
                    user = self.bot.get_user(int(USERDM[Cursor][0]))
                    if user != None:
                        S1Name, S1Brand, S1Cost, S1Skill, S1Ability, S1Icon, S1End = splat_file['merchandises'][5]['gear']['name'], splat_file['merchandises'][5]['gear']['brand']['name'], splat_file['merchandises'][5]['price'], splat_file['merchandises'][5]['skill']['name'], splat_file['merchandises'][5]['gear']['brand']['frequent_skill']['name'], splat_file['merchandises'][5]['gear']['image'], datetime.fromtimestamp(splat_file['merchandises'][5]['end_time']).ctime()
                        embed=discord.Embed(color=discord.Colour.orange(), title=f'Requested Item is in SplatNet2! {S1Name} ({S1Brand})')
                        embed.add_field(name=f'Gear Price', value=f'<:Coin:460630467364913152> `{S1Cost}`', inline=True)
                        embed.add_field(name=f'Sale Ends At', value=f'`{S1End}`', inline=True)
                        embed.add_field(name=f'Main Ability', value=f'`{S1Skill}`', inline=True)
                        embed.add_field(name=f'Common Ability ({S1Brand})', value=f'`{S1Ability}`', inline=True)
                        embed.set_thumbnail(url=f'https://splatoon2.ink/assets/splatnet{S1Icon}')
                        embed.set_footer(text='Information Grabbed From splatoon2.ink')
                        await user.send(embed=embed)
                except:
                    pass
                Cursor += 1

    async def splatnet_loop(self):
        await self.bot.wait_until_ready()
        while True:
            await asyncio.sleep(15)
            now = datetime.now()
            if now.minute == 1:
                print('Checking Auto-Updater!')
                await self.splatnet_check()
                await self.auto_splatnet_check()
                await asyncio.sleep(60)

    async def grizzco_loop(self):
        await self.bot.wait_until_ready()
        while True:
            await asyncio.sleep(15)
            now = datetime.now()
            if now.minute == 1:
                print('Checking Auto-Updater!')
                await self.grizzco_check()
                await asyncio.sleep(60)

    async def rotation_loop(self):
        await self.bot.wait_until_ready()
        while True:
            await asyncio.sleep(15)
            now = datetime.now()
            if now.minute == 1:
                print('Checking Auto-Updater!')
                await self.rotation_check()
                await asyncio.sleep(60)

    @commands.group(name='splatoon2')
    async def splatoon2_ink(self, ctx):
        pass

    @splatoon2_ink.command(name='gamemode', case_insensitive=True)
    async def splatoon2_ink_gamemode(self, ctx, rotation: int, *, gamemode):
        if ctx.message.author.bot == True:
            return
        else:
            GameURL = 'https://splatoon2.ink/data/schedules.json'
            GameMode = requests.get(GameURL)
            game_file = GameMode.json()
            if gamemode.lower() in gamemode_list:
                GMC = gamemode_converter[gamemode.lower()]
                try:
                    Map1N, Map2N = game_file[GMC][rotation + 1]['stage_a']['name'], game_file[GMC][rotation + 1]['stage_b']['name']
                    GameModeN = game_file[GMC][rotation + 1]['rule']['name']
                    StartTimeN, EndTimeN = datetime.fromtimestamp(game_file[GMC][rotation + 1]['start_time']).ctime(), datetime.fromtimestamp(game_file[GMC][rotation + 1]['end_time']).ctime()
                    Map1, Map2 = game_file[GMC][rotation]['stage_a']['name'], game_file[GMC][rotation]['stage_b']['name']
                    GameMode = game_file[GMC][rotation]['rule']['name']
                    StartTime, EndTime = datetime.fromtimestamp(game_file[GMC][rotation]['start_time']).ctime(), datetime.fromtimestamp(game_file[GMC][rotation]['end_time']).ctime()
                except:
                    try:
                        Map1N, Map2M, = 'Unknown', 'Unknown'
                        StartTimeN, EndTimeN = 'Unknown', 'Unknown'
                        GamemodeN = 'Unknown'
                        Map1, Map2 = game_file[GMC][rotation]['stage_a']['name'], game_file[GMC][rotation]['stage_b']['name']
                        GameMode = game_file[GMC][rotation]['rule']['name']
                        StartTime, EndTime = datetime.fromtimestamp(game_file[GMC][rotation]['start_time']).ctime(), datetime.fromtimestamp(game_file[GMC][rotation]['end_time']).ctime()
                    except:
                        embed=discord.Embed(color=discord.Colour.red())
                        embed.add_field(name=f"Unknown Information", value=f'Information could not be grabbed from Splatoon2.ink!', inline=False)
                        return await ctx.send(embed=embed)
                FileQuery = gamemode.split(' ')[0]
                f = discord.File(f"{self.bot.directory}/images/gamemode_icon/{FileQuery}.png", f"{FileQuery}.png") 
                embed=discord.Embed(color=discord.Colour.red())
                embed.add_field(name=f"Current {gamemode_conv_name[gamemode.lower()]} Rotation Active Through", value=f'`{StartTime} - {EndTime}`', inline=False)
                embed.add_field(name=f"Current {gamemode_conv_name[gamemode.lower()]} Gamemode", value=f'`{GameMode}`', inline=True)
                embed.add_field(name=f"Current {gamemode_conv_name[gamemode.lower()]} Maps", value=f'`{Map1}`\n`{Map2}`', inline=True)
                embed.add_field(name=f"Next Rotation Active Through", value=f'`{StartTimeN} - {EndTimeN}`', inline=False)
                embed.set_thumbnail(url=f"attachment://{FileQuery}.png")
                embed.set_footer(text='Information Grabbed From splatoon2.ink')
                await ctx.send(file=f, embed=embed)
            else:
                embed=discord.Embed(color=discord.Colour.orange(), )
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                embed.add_field(name='Invalid Gamemode', value=f"*[ERROR_INVALID_GAMEMODE]*", inline=False)
                await ctx.send(embed=embed)


    @splatoon2_ink.command(name='grizzco', case_insensitive=True)
    async def splatoon2_ink_grizzco(self, ctx):
        if ctx.message.author.bot == True:
            return
        else:
            GrizzURL = 'https://splatoon2.ink/data/coop-schedules.json'
            GrizzCo = requests.get(GrizzURL)
            grizz_file = GrizzCo.json()
            GrizzTime, GrizzEnd = datetime.fromtimestamp(grizz_file['details'][0]['start_time']).ctime(), datetime.fromtimestamp(grizz_file['details'][0]['end_time']).ctime()
            GrizzTimeN, GrizzEndN = datetime.fromtimestamp(grizz_file['details'][1]['start_time']).ctime(), datetime.fromtimestamp(grizz_file['details'][1]['end_time']).ctime()
            GrizzMap, GrizzMapN, = grizz_file['details'][0]['stage']['name'], grizz_file['details'][1]['stage']['name']
            GrizzIcon = grizz_file['details'][0]['stage']['image']
            try:
                GrizzWep1 = grizz_file['details'][0]['weapons'][0]['weapon']['name']
                GrizzSub1 = grizz_file['details'][0]['weapons'][0]['weapon']['sub']['name']
                GrizzSpecial1 = grizz_file['details'][0]['weapons'][0]['weapon']['special']['name']
            except:
                GrizzWep1 = 'Random'
                GrizzSub1 = 'Unknown'
                GrizzSpecial1 = 'Unknown'
            try:
                GrizzWep2 = grizz_file['details'][0]['weapons'][1]['weapon']['name']
                GrizzSub2 = grizz_file['details'][0]['weapons'][1]['weapon']['sub']['name']
                GrizzSpecial2 = grizz_file['details'][0]['weapons'][1]['weapon']['special']['name']
            except:
                GrizzWep2 = 'Random'
                GrizzSub2 = 'Unknown'
                GrizzSpecial2 = 'Unknown'
            try:
                GrizzWep3 = grizz_file['details'][0]['weapons'][2]['weapon']['name']
                GrizzSub3 = grizz_file['details'][0]['weapons'][2]['weapon']['sub']['name']
                GrizzSpecial3 = grizz_file['details'][0]['weapons'][2]['weapon']['special']['name']
            except:
                GrizzWep3 = 'Random'
                GrizzSub3 = 'Unknown'
                GrizzSpecial3 = 'Unknown'
            try:
                GrizzWep4 = grizz_file['details'][0]['weapons'][3]['weapon']['name']
                GrizzSub4 = grizz_file['details'][0]['weapons'][3]['weapon']['sub']['name']
                GrizzSpecial4 = grizz_file['details'][0]['weapons'][3]['weapon']['special']['name']
            except:
                GrizzWep4 = 'Random'
                GrizzSub4 = 'Unknown'
                GrizzSpecial4 = 'Unknown'
            embed=discord.Embed(color=discord.Colour.orange())
            embed.add_field(name=f"Latest Salmon Run Information ({GrizzMap})", value=f'`{GrizzTime} - {GrizzEnd} - UTC/GMT`', inline=True)
            embed.add_field(name=f"Weapons", value=f'`{GrizzWep1} ({GrizzSub1}) ({GrizzSpecial1})`\n`{GrizzWep2} ({GrizzSub2}) ({GrizzSpecial2})`\n`{GrizzWep3} ({GrizzSub3}) ({GrizzSpecial3})`\n`{GrizzWep4} ({GrizzSub4}) ({GrizzSpecial4})`', inline=False)
            embed.add_field(name=f"Next Salmon Run ({GrizzMapN})", value=f'`{GrizzTimeN} - {GrizzEndN}`', inline=False)
            embed.set_image(url=f'https://splatoon2.ink/assets/splatnet{GrizzIcon}')
            embed.set_footer(text='Information Grabbed From splatoon2.ink')
            await ctx.send(embed=embed)

    @splatoon2_ink.command(name='splatnet', case_insensitive=True)
    async def splatoon2_ink_splatnet(self, ctx):
        """Displays the Current SplatNet2 Gear"""
        if ctx.message.author.bot == True:
            return
        else:
            SplatURL = 'https://splatoon2.ink/data/merchandises.json'
            SplatNet2 = requests.get(SplatURL)
            splat_file = SplatNet2.json()
            Run = True
            Cursor = 0
            for item in splat_file['merchandises']:
                S1Name, S1Brand, S1Cost, S1Skill, S1Ability, S1Icon, S1End = splat_file['merchandises'][Cursor]['gear']['name'], splat_file['merchandises'][Cursor]['gear']['brand']['name'], splat_file['merchandises'][Cursor]['price'], splat_file['merchandises'][Cursor]['skill']['name'], splat_file['merchandises'][Cursor]['gear']['brand']['frequent_skill']['name'], splat_file['merchandises'][Cursor]['gear']['image'], datetime.fromtimestamp(splat_file['merchandises'][Cursor]['end_time']).ctime()
                embed=discord.Embed(color=discord.Colour.orange(), title=f'{S1Name} ({S1Brand})')
                embed.add_field(name=f'Gear Price', value=f'<:Coin:460630467364913152> `{S1Cost}`', inline=True)
                embed.add_field(name=f'Sale Ends At', value=f'`{S1End}`', inline=True)
                embed.add_field(name=f'Main Ability', value=f'`{S1Skill}`', inline=True)
                embed.add_field(name=f'Common Ability ({S1Brand})', value=f'`{S1Ability}`', inline=True)
                embed.set_thumbnail(url=f'https://splatoon2.ink/assets/splatnet{S1Icon}')
                embed.set_footer(text='Information Grabbed From splatoon2.ink')
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
                Cursor += 1
        

def setup(bot):
    bot.add_cog(Splatoon2_Ink(bot))