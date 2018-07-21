import random
import asyncio
from discord.ext import commands
from utils import formatter
from discord import Embed
import discord

coinFlip = [
    'https://cdn.discordapp.com/attachments/448341812055244817/448502226021908490/coinsmalltails.png',
    'https://cdn.discordapp.com/attachments/448341812055244817/448502223589212160/coinsmall.png'
]

five_stars = [
    "bastet",
    "mafdet",
    "charles",
    "ashtoreth",
    "cleopatra",
    "hildr",
    "cube_moa",
    "apep",
    "nirrti",
    "aria",
    "sitri",
    "luna",
    "neptune",
    "diablo",
    "dana",
    "horus",
    "maat",
    "venus",
    "elizabeth",
    "kubaba",
    "frey",
    "yan",
    "d_maat",
    "mars",
    "lanfei",
    "rita",
    "pantheon",
    "semele",
    "warwolf",
    "ai",
    "redcross",
    "medusa",
    "metis",
    "hestia",
    "medb",
    "saladin",
    "morgan",
    "tyrfing",
    "demeter",
    "jupiter",
    "hermes",
    "red_queen",
    "verdel",
    "hades",
    "dinashi",
    "aurora",
    "deino",
    "thanatos",
    "eve",
    "bari",
    "d_lisa",
    "saturn",
    "wola",
    "santa",
    "babel",
    "myrina",
    "isolde",
    "naias",
    "sang_ah",
    "willow",
    "anemone",
    "ymir",
    "maris",
    "eshu",
    "rusalka",
    "siren",
    "gd_sang_ah",
    "abaddon",
    "nicole",
    "krampus",
    "jcb",
    "daphnis",
    "midas",
    "ruin",
    "epona",
    "hera",
    "mammon",
    "brownie",
    "newbie_mona",
    "bathory",
    "syrinx",
    "astrea",
]

world_bosses = [
    'Aria',
    'Cleo',
    'Apep',
    'Isolde',
    'Khepri',
    'Nicole',
    'Thetis',
    'Demeter',
    'Rita',
    'Slime',
    'Morgan',
    'Krampus',
    'Bari',
]

quotes = [
    'Signs point to yes.',
    'Yes.',
    'Reply hazy, try again.',
    'My sources say no.',
    'You may rely on it.',
    'Concentrate and ask again.',
    'Outlook not so good.',
    'It is decidedly so.',
    'Better not tell you now.',
    'Very doubtful.',
    'Yes - definitely.',
    'It is certain.',
    'Cannot predict now.',
    'Most likely.',
    'Ask again later.',
    'My reply is no.',
    'Outlook good.',
    "Don't count on it."
]

slaps = [
    'slaps {} around a bit with a large trout',
    'gives {} a clout round the head with a fresh copy of WeeChat',
    'slaps {} with a large smelly trout',
    'breaks out the slapping rod and looks sternly at {}',
    "slaps {}'s bottom and grins cheekily",
    'slaps {} a few times',
    'slaps {} and starts getting carried away',
    'would slap {}, but (s)he is too lazy to do it.',
    'gives {} a hearty slap',
    'finds the closest large object and gives {} a slap with it',
    'likes slapping people and randomly picks {} to slap',
    'dusts off a kitchen towel and slaps it at {}',
    'breaks the 4th wall and slaps {} with the pieces of it.',
    'slaps {} with a b grade stop sign.',
    'slaps {} with a baguette that still freshly baked.'
    'got a whip from chest. Time to try it, {} will be the target.'
]

class FunCog:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def eight_ball(self, ctx):
        """Ask the great 8ball for answer."""

        if ctx.message.channel.id == 167280538695106560 or ctx.message.channel.id == 360916876986941442:
            await ctx.send(random.choice(quotes))
        else:
            await ctx.message.delete()
            await ctx.author.send("My mystical ball only works on channels with rich magic like`i-am-bot`")

    @commands.command(name='choose', aliases=['choice', 'pick'])
    async def choose(self, ctx, *, args):
        """Choose one or another args:<option> , <option2> [, <option3>...]"""
        if ctx.message.channel.id == 167280538695106560 or ctx.message.channel.id == 360916876986941442:
            split_message = args.split(',')
            await ctx.send(random.choice(split_message))
        else:
            await ctx.message.delete()
            await ctx.author.send("This command is locked to `i-am-bot`.")

    @commands.command(name='coin', aliases=['flip'])
    async def flip_coin(self,ctx):
        """Flip a coin."""
        em = await formatter.coin_embed(random.choice(coinFlip))
        m = await ctx.send(embed=em)
        await asyncio.sleep(8)
        await ctx.message.delete()
        await m.delete()

    @commands.command(name='slap')
    async def slap(self, ctx, mention: discord.Member):
        """Slap someone. args: <mention>"""
        em = Embed(description=ctx.author.display_name + " " + random.choice(slaps).format(mention.display_name))
        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command(name='gacha', aliases=['gatcha'])
    async def gacha(self, ctx, *args):
        """Chooses a random 5* that can be get from gacha. args: [wb]"""
        if args:
            if args[0] == 'wb':
                em = Embed(description=ctx.author.display_name + " thinks that the world boss will be " + random.choice(world_bosses))
        else:
            em = Embed(description=ctx.author.display_name + " guessed " + random.choice(five_stars))
        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command(name='user', aliases=['userinfo', 'info', 'ui', 'uinfo'])
    @commands.guild_only()
    async def user_info(self,ctx, *args):
        """returns mentioned user info. Aliases: userinfo, info, ui, uinfo"""
        if ctx.message.channel.id == 167280538695106560 or ctx.message.channel.id == 360916876986941442:
            if args:
                user = ctx.message.mentions[0]
            else:
                user = ctx.author

            if user.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = user.avatar_url.rsplit("?", 1)[0]
            else:
                avi = user.avatar_url_as(static_format='png')

            em = Embed(timestamp=ctx.message.created_at)
            em.add_field(name='Nick', value=user.display_name, inline=False)
            em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
            em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
            em.set_thumbnail(url=avi)
            em.set_footer(text=f'Invoked by: {ctx.author.display_name}')
            await ctx.message.delete()
            await ctx.send(embed=em)
        else:
            await ctx.message.delete()
            await ctx.author.send("Don't use it outside of bot channel.")


def setup(bot):
    bot.add_cog(FunCog(bot))
