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

class Profile:
    """Profile System"""

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    def profile_check():
        async def profile_exist(ctx):
            conn = sqlite3.connect(f'splatoon-bot.db', timeout=8)
            cur = conn.cursor()
            cur.execute('SELECT ID FROM Profile WHERE ID=?', (ctx.message.author.id,))
            user_in_db = cur.fetchone()
            cur.close()
            if user_in_db:
                return True
            else:
                embed=discord.Embed(color=discord.Colour.blue(), description='Profile Does Not Exist')
                embed.set_author(name=config.name, icon_url='https://cdn.discordapp.com/attachments/458442870873915392/460973473154596864/phone.png')
                await ctx.send(embed=embed)
                return False
        return commands.check(profile_exist)

    def bot_user_check():
        async def bot_user(ctx):
            if ctx.message.author.bot == True:
                return False
            else:
                return True
        return commands.check(bot_user)

    @commands.group(aliases=['profil', 'account'], invoke_without_command=True, ignore_extra=False, case_insensitive=True)
    @profile_check()
    @bot_user_check()
    async def profile(self, ctx, user: discord.Member=None):
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        if user == None:
            cur.execute('SELECT IGN, FC, Level, RM, SZ, TC, CB, Banner FROM Profile WHERE ID=?', (ctx.message.author.id,))
            IGN, FC, Level, RM, SZ, TC, CB, Banner = cur.fetchone()
            embed=discord.Embed(color=discord.Colour.teal(), title=f"{ctx.message.author.name}'s Profile")
            embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
            embed.add_field(name=f'Username:', value=f'{IGN}', inline=True)
            embed.add_field(name=f'Friend Code', value=f'{FC}', inline=True)
            embed.add_field(name=f'Ranked Statistics', value=f'Rainmaker: {RM}\nTower Control: {TC}\nSplat Zones: {SZ}\nClam Blitz: {CB}', inline=True)
            embed.add_field(name=f'Level', value=f'Level: {Level}', inline=True)
            embed.set_image(url=Banner)
            await ctx.send(embed=embed)
        else:
            Check = self.bot.get_user(user.id)
            if not Check == None:
                try:
                    cur.execute('SELECT IGN, FC, Level, RM, SZ, TC, CB, Banner FROM Profile WHERE ID = {0.id}'.format(user))
                    IGN, FC, Level, RM, SZ, TC, CB, Banner = cur.fetchone()
                    embed=discord.Embed(color=discord.Colour.teal(), title=f"{user.name}'s Profile")
                    embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                    embed.add_field(name=f'Username:', value=f'{IGN}', inline=True)
                    embed.add_field(name=f'Friend Code', value=f'{FC}', inline=True)
                    embed.add_field(name=f'Ranked Statistics', value=f'Rainmaker: {RM}\nTower Control: {TC}\nSplat Zones: {SZ}\nClam Blitz: {CB}', inline=True)
                    embed.add_field(name=f'Level', value=f'Level: {Level}', inline=True)
                    embed.set_image(url=Banner)
                    await ctx.send(embed=embed)
                except:
                    embed=discord.Embed(color=discord.Colour.teal())
                    embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url, description='User Does Not Exist')
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=discord.Colour.teal())
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url, description='User Does Not Exist')
                await ctx.send(embed=embed)
        cur.close()
    
    @profile.command(ignore_extra=False, case_insensitive=True)
    @bot_user_check()
    async def create(self, ctx):
        """Creates a User Profile"""
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        cur.execute('SELECT ID FROM Profile WHERE ID = ?', (ctx.message.author.id,))
        result = cur.fetchone()
        if not result:
            cur.execute('INSERT INTO Profile(ID, IGN, Level, FC, RM, SZ, TC, CB, Banner) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (ctx.message.author.id, 'Unset', '1', 'SW-0000-0000-0000', 'C-', 'C-', 'C-', 'C-', random.choice(self.bot.config.banner_list),))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.teal(), description=f"{ctx.message.author.mention} your profile has been created!")
            embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
            message = await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=discord.Colour.teal(), description=f'You already have a Profile {ctx.message.author.mention}!')
            embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
            await ctx.send(embed=embed)
        cur.close() 

    @profile.command(aliases=['name', 'username'], invoke_without_command=True, ignore_extra=False, case_insensitive=True)
    @profile_check()
    @bot_user_check()
    async def ign(self, ctx, *, ign):
        """Sets your Username"""
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        if len(ign) > 12:
            embed=discord.Embed(color=discord.Colour.teal(), )
            embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
            embed.add_field(name='Unsupported Length:', value=f"Switch Username Rules! Username cannot be more than 12 Characters", inline=False)
            message = await ctx.send(embed=embed)
        else:
            cur.execute('UPDATE Profile SET IGN=? WHERE ID=?', (ign, ctx.message.author.id,))
            conn.commit()
            embed=discord.Embed(color=discord.Colour.teal(), )
            embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
            embed.add_field(name='Username Set:', value=f"{ctx.message.author.name} has set their Username to {ign}!", inline=False)
            message = await ctx.send(embed=embed)      
        cur.close()   


    @profile.command(aliases=['code'], invoke_without_command=True, ignore_extra=False, case_insensitive=True)
    @profile_check()
    @bot_user_check()
    async def fc(self, ctx, friend, code, here):
        """Sets your Switch-Friend-Code"""
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        try:
            lencheck = len(friend) + len(code) + len(here)
            strfriend, strcode, strhere = str(friend), str(code), str(here)
            friend, code, here = int(friend), int(code), int(here)
            if lencheck == 12:
                cur.execute('UPDATE Profile SET FC=? WHERE ID=?', (f'SW-{strfriend}-{strcode}-{strhere}', ctx.message.author.id,))
                conn.commit()
                embed=discord.Embed(color=discord.Colour.teal(), )
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Friend Code Set:', value=f"{ctx.message.author.name}'s Friend code has been set to SW-{strfriend}-{strcode}-{strhere}!", inline=False)
                message = await ctx.send(embed=embed) 
            else:
                embed=discord.Embed(color=discord.Colour.teal(), )
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Not 4 in Length:', value=f"{ctx.message.author.name} *[ERROR_Length_Not_4]*", inline=False)
                message = await ctx.send(embed=embed) 
        except ValueError:
            if len(str(friend)) > 4 and len(str(code)) > 4 and len(str(here)) > 4:
                embed=discord.Embed(color=discord.Colour.teal(), )
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Friend Code is Not a Integer & 4 in Length:', value=f"{ctx.message.author.name} *[ERROR_Not_Integer_Or_Length_Of_4]*", inline=False)
                message = await ctx.send(embed=embed) 
            else:
                embed=discord.Embed(color=discord.Colour.teal(), )
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Friend Code is Not a Integer:', value=f"{ctx.message.author.name} *[ERROR_Not_Integer]*", inline=False)
                message = await ctx.send(embed=embed) 
        cur.close()   
    
    @profile.command(case_insensitive=True)
    @profile_check()
    @bot_user_check()
    async def level(self, ctx, level):
        """Sets your Level (*Level is Supported)"""
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        try:
            level = int(level)
            if level > 198:
                embed=discord.Embed()
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Max Level', value=f"*[ERROR_MAX_LEVEL_*99]*", inline=False)
                message = await ctx.send(embed=embed)
            else:
                if level > 99:
                    level = level - 99
                    level = f'*{level}'
                cur.execute('UPDATE Profile SET Level=? WHERE ID=?', (level, ctx.message.author.id,))
                conn.commit()
                embed=discord.Embed(color=discord.Colour.teal(), )
                embed.set_author(name=f"{self.bot.config.name}", icon_url=self.bot.config.url)
                embed.add_field(name='Level has been Successfully Set!', value=f"{ctx.message.author.name} has set their level to {level}!", inline=False)
                message = await ctx.send(embed=embed) 
        except ValueError:
            embed=discord.Embed(color=discord.Colour.teal(), )
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            embed.add_field(name='Level is Not a Integer:', value=f"{ctx.message.author.name} *[ERROR_Not_Integer]*", inline=False)
            message = await ctx.send(embed=embed) 
    
    @profile.command(case_insensitive=True)
    async def rank(self, ctx, gamemode, *, rank):
        """Sets your Competitive Gamemode Ranks"""
        game_mode = ['cb', 'tc', 'sz', 'rm']
        rank_list = ['c-', 'c', 'c+', 'b-', 'b', 'b+', 'a-', 'a', 'a+', 's', 's+0', 's+1', 's+2', 's+3', 's+4', 's+5', 's+6', 's+7', 's+8', 's+9', 'x']
        conn = sqlite3.connect(f'{self.bot.directory}/splatoon-bot.db')
        cur = conn.cursor()
        if gamemode.lower() in game_mode:
            if rank.lower() in rank_list:
                cur.execute(f'UPDATE Profile SET {gamemode.upper()}=? WHERE ID=?', (rank.upper(), ctx.message.author.id,))
                conn.commit()
                embed=discord.Embed(color=discord.Colour.teal(), description=f'{ctx.message.author.mention} has set their {gamemode.upper()} rank to {rank.upper()}!')
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                await ctx.send(embed=embed) 
            else:
                ValidRank = '\n'
                for item, index in rank_list:
                    ValidRank += f'\n{rank_list[index]}'
                embed=discord.Embed(color=discord.Colour.teal(), description=f'{ctx.message.author.name} **{gamemode.upper()}** is not a Valid Rank!\n```VALID RANK LIST:{ValidRank}```')
                embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
                await ctx.send(embed=embed) 
        else:
            embed=discord.Embed(color=discord.Colour.teal(), description=f'{ctx.message.author.name} **{gamemode.upper()}** is not a Valid Gamemode!\n```VALID GAMEMODE LIST:\nRM\nTC\nSZ\nCB```')
            embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
            await ctx.send(embed=embed) 


def setup(bot):
    bot.add_cog(Profile(bot))