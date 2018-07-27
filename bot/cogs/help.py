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
from mutagen.mp3 import MP3

Connection = {}

class Cog:
    """Cog for Cog related commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, ignore_extra=False, case_insensitve=True)
    async def help(self, ctx):
        try:
            Prefix = self.bot.prefix_dict.get(ctx.message.guild.id, ".")
        except:
            Prefix = '.'
        embed=discord.Embed(color=discord.Colour.blurple(), title='Bot Module Information', description=f'__**Profile - Module**__\n\n`The Main Feature of {self.bot.config.name}, Allows users to set profile information`\n\n__**Splatoon2 - Module**__\n\n`Displays SplatNet2, GrizzCo, and Rotation Information`\n\n__**Utility - Module**__\n\n`Callouts, Collectable Viewers, and other Splatoon Utilities`')
        embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
        embed.set_footer(text=f"Need Information on a Module? type {Prefix}help <Module>")
        await ctx.send(embed=embed)

    @help.group(aliases=['utility', 'utilities'], ignore_extra=False, case_insensitve=True)
    async def help_utility(self, ctx):
        try:
            Prefix = self.bot.prefix_dict.get(ctx.message.guild.id, ".")
        except:
            Prefix = '.'
        embed=discord.Embed(color=discord.Colour.dark_grey(), title='Utility Module Command List', description=f'__**{Prefix}utility callout <view> <map>**__\n\n`Displays Callouts for the Specified Map`\n`Example: {Prefix}utility callout overview reef`\n\n__**{Prefix}utility splatnet-add**__\n\n`Sets the current channel to a Automatic SplatNet2 Channel`\n`Example: {Prefix}utility splatnet-add`\n\n__**{Prefix}utility grizzco-add**__\n\n`Sets the current channel to a Automatic GrizzCo Channel`\n`Example: {Prefix}utility grizzco-add`\n\n__**{Prefix}utility rotation-add**__\n\n`Sets the current channel to a Automatic Rotation Channel`\n`Example: {Prefix}utility rotation-add`\n\n__**{Prefix}utility mem <index>**__\n\n`Displays the Specified Mem Cake`\n`Example: {Prefix}utility mem 1`\n\n__**{Prefix}utility prefix <prefix>**__\n\n`Changes/Sets Guild Prefix`\n`Example: {Prefix}utility prefix --`')
        embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
        embed.set_footer(text=f"Credits to @VeeMOE#2164 For Making the Program!")
        await ctx.send(embed=embed)

    @help.group(name='profile', ignore_extra=False, case_insensitve=True)
    async def helpprofile(self, ctx):
        try:
            Prefix = self.bot.prefix_dict.get(ctx.message.guild.id, ".")
        except:
            Prefix = '.'
        embed=discord.Embed(color=discord.Colour.teal(), title='Profile Module Command List', description=f"__**{Prefix}profile <optional: user>**__\n\n`Displays a Users Profile`\n`Note: Bot will display your profile if a user is not specified`\n`Example: {Prefix}profile`\n`Alternate Example: {Prefix}profile VeeMOE`\n\n__**{Prefix}profile create**__\n\n`Creates a Profile if none already Exists`\n`Example: {Prefix}profile create`\n\n__**{Prefix}profile ign <username>**__\n\n`Sets your Username`\n`Example: {Prefix}profile ign Telephone`\n\n__**{Prefix}profile fc <friend> <code> <here>**__\n\n`Sets your Switch-Friend-Code`\n`Example: {Prefix}profile fc 2798 6276 2687`\n\n__**{Prefix}profile level <level>**__\n\n`Sets your Level`\n`Note: *Rank is Supported! Just Specify a Level Above 99`\n`Example: {Prefix}profile level 50`\n\n__**{Prefix}profile rank <gamemode> <rank>**__\n\n`Sets your Ranked Level`\n`Note: Rank X is supported! Just Specify X and a Power`\n`Example: {Prefix}profile rank rainmaker S+3`\n`Alternate Example: {Prefix}profile rank rainmaker X 1500`")
        embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
        embed.set_footer(text=f"Credits to @VeeMOE#2164 For Making the Program!")
        await ctx.send(embed=embed)

    @help.group(name='splatoon2', ignore_extra=False, case_insensitve=True)
    async def helpsplatoon2(self, ctx):
        try:
            Prefix = self.bot.prefix_dict.get(ctx.message.guild.id, ".")
        except:
            Prefix = '.'
        embed=discord.Embed(color=discord.Colour.orange(), title='Splatoon2.ink Module Command List', description=f'__**{Prefix}splatoon2 gamemode <rotation> <game mode>**__\n\n`Displays Information on the Specified Gamemode Rotation`\n`{Prefix}splatoon2 gamemode 0 turf war`\n\n__**{Prefix}splatoon2 gamemode grizzco**__\n\n`Displays the Latest Salmon Run Rotation`\n`{Prefix}splatoon2 grizzco`\n\n__**{Prefix}splatoon2 splatnet**__\n\n`Displays all items that are Available in SplatNet2`\n`{Prefix}splatoon2 splatnet`')
        embed.set_author(name=self.bot.config.name, icon_url=self.bot.config.url)
        embed.set_footer(text=f"Credits to @VeeMOE#2164 For Making the Program!")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Cog(bot))