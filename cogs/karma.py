import asyncio

import discord
from discord.ext import commands

from service.userService import UserService
from utils.helpers import checkdigitarguments


def is_admin(ctx):
    if ctx.author.id == 114010253938524167 or ctx.author.id == 224522663626801152:
        return True
    else:
        return False


class KarmaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.userS = UserService(self.bot)

    async def member_exist(self, target):
        user = await self.userS.getuser(target.id)
        if not user:
            await self.userS.adduser(target.id)

    @commands.command(name="karma", aliases=['k'])
    async def karma(self, ctx, *args):
        """Kirinus karma system. [?k] (add/remove/balance) [optional for balance: @targetMention] [optional:value]"""
        em = discord.Embed()
        m = None
        if len(args) < 1:
            em.description = "Use ?karma[?k] (add/remove/balance) [optional for balance: @targetMention] [optional:value]"
            m = await ctx.send(embed=em)
        else:
            target = ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else ctx.author

            if args[0].lower() == "add" and len(ctx.message.mentions) > 0 and is_admin(ctx):
                value = checkdigitarguments(args, 1)
                await self.member_exist(target)
                await self.userS.addkarma(target.id, value)
                em.description = f"User {target.mention} received {value} karma points."
                m = await ctx.send(embed=em)

            elif args[0].lower() == "remove" and len(ctx.message.mentions) > 0 and is_admin(ctx):
                value = checkdigitarguments(args, 1)
                await self.member_exist(target)
                await self.userS.removekarma(target.id, value)
                em.description = f"User {target.mention} lost {value} karma points."
                m = await ctx.send(embed=em)

            elif args[0].lower() == "balance":
                await self.member_exist(target)
                value = await self.userS.userbalance(target.id)
                em.description = f"{target.display_name}'s balance: {value['karma']}"
                m = await ctx.send(embed=em)

        await asyncio.sleep(5)
        await ctx.message.delete()
        if m:
            await m.delete()


def setup(bot):
    bot.add_cog(KarmaCog(bot))