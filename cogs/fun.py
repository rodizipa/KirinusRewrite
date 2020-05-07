import asyncio
import random

import discord
from discord import Embed
from discord.ext import commands

from utils import formatter, helpers

coinFlip = [
    'https://cdn.discordapp.com/attachments/448341812055244817/448502226021908490/coinsmalltails.png',
    'https://cdn.discordapp.com/attachments/448341812055244817/448502223589212160/coinsmall.png'
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


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @helpers.bot_channel()
    @commands.command('8ball')
    async def eight_ball(self, ctx):
        """Ask the great 8ball for answer."""
        await ctx.send(random.choice(quotes))

    @eight_ball.error
    async def eight_ball_error(self, ctx, error):
        if isinstance(error, helpers.WrongChannel):
            await helpers.message_denied("My mystical ball only works on channels with rich magic like`i-am-bot`", \
                                         ctx, True)

    @helpers.bot_channel()
    @commands.command(name='choose', aliases=['choice', 'pick'])
    async def choose(self, ctx, *, args):
        """Choose one or another args:<option> , <option2> [, <option3>...]"""
        split_message = args.split(',')
        await ctx.send(random.choice(split_message))

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, helpers.WrongChannel):
            await helpers.message_denied("This command is locked to `i-am-bot`.", ctx, True)

    @commands.command(name='coin', aliases=['flip'])
    async def flip_coin(self, ctx):
        """Flip a coin."""
        em = await formatter.coin_embed(random.choice(coinFlip))
        await helpers.message_handler(em, ctx, 8, True)

    @commands.command(name='slap')
    async def slap(self, ctx, mention: discord.Member):
        """Slap someone. args: <mention>"""
        em = Embed(description=ctx.author.display_name + " " + random.choice(slaps).format(mention.display_name))
        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command(name="insult")
    async def insult(self, ctx):
        await formatter.random_insult(ctx)

    @commands.command(name='userinfo', aliases=['info', 'ui', 'uinfo'])
    async def user_information(self, ctx, *, member: discord.Member = None):
        """returns mentioned user info. Aliases: userinfo, info, ui, uinfo"""
        user = member if member else ctx.author

        avi = user.avatar_url

        em = Embed(timestamp=ctx.message.created_at)
        em.add_field(name='Nick', value=user.display_name, inline=False)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
        em.set_thumbnail(url=avi)
        em.set_footer(text=f'Invoked by: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=em)

    @user_information.error
    async def user_info(self, ctx, error):
        if isinstance(error, helpers.WrongChannel):
            await helpers.message_denied("Don't use it outside of bot channel.", ctx, True)
        else:
            await ctx.send(error.__cause__)
            print(error.__cause__)

    @commands.command(name="poll", aliases=['p'])
    async def poll(self, ctx, *, msg):
        """Create poll using [,] as delimiter. [Question], [answer1],...,[answer9], time=[minutes]"""
        await asyncio.sleep(1)
        await ctx.message.delete()

        options = msg.split(',')

        time = [x for x in options if x.startswith("time=")]

        if time:
            time = time[0]
            options.remove(time)

        if (len(options) < 3) or (len(options) > 11):
            return await ctx.send("Min 2 options, Max 9.")

        time = int(time.strip("time=")) if time else 60

        emoji = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
        to_react = []
        em = discord.Embed(title=f"**{options[0]}**")
        em.set_footer(text=f"Created by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        confirm_msg = ""
        #  add options
        for index, option in enumerate(options[1:]):
            confirm_msg += f"{emoji[index]} - {option}\n"
            to_react.append(emoji[index])
        confirm_msg += f"\n\nYou have {time} seconds to vote!"
        em.description = confirm_msg
        poll_msg = await ctx.send(embed=em)

        for emote in to_react:
            await poll_msg.add_reaction(emote)

        await asyncio.sleep(time)

        async for message in ctx.message.channel.history():
            if message.id == poll_msg.id:
                poll_msg = message

        results = {}

        for reaction in poll_msg.reactions:
            if reaction.emoji in to_react:
                results[reaction.emoji] = reaction.count - 1

        em2 = discord.Embed(title=f"{em.title}")
        end_msg = "The poll ended. Here the results:\n\n"
        for result in results:
            end_msg += f"{result} {options[emoji.index(result) + 1]} - {results[result]} votes\n"
        top_result = max(results, key=lambda key: results[key])
        if len([x for x in results if results[x] == results[top_result]]) > 1:
            top_results = []
            for key, value in results.items():
                if value == results[top_result]:
                    top_results.append(options[emoji.index(key) + 1])
            tied = ", ".join(top_results)
            if max(results.values()) == 0:
                end_msg += "\nBah, nobody voted"
            else:
                end_msg += f"\nVictory tied between {tied}"
        else:
            top_result = options[emoji.index(top_result) + 1]
            end_msg += f"\n{top_result} is the winner!"
        em2.description = end_msg
        await ctx.send(embed=em2)

    @commands.command(name="random")
    async def random_n(self, ctx, start: int, end: int):
        await ctx.send(random.randint(start, end))

    @commands.command(name="rlist", aliases=['rl'])
    async def random_list(self, ctx, amount: int):

        l1 = [str(i + 1) for i in range(amount)]
        random.shuffle(l1)
        em = discord.Embed(description="||" + " ".join(l1) + "||", color=discord.colour.Color.blue())
        await ctx.send(embed=em)
        await asyncio.sleep(1)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(FunCog(bot))
