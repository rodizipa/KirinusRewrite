from asyncio import sleep

from discord.ext import commands


class WrongChannel(commands.CheckFailure):
    pass


def bot_channel():
    async def predicate(ctx):
        if ctx.message.channel.id in (167280538695106560, 360916876986941442, 378255860377452545, 458755509890056222):
            return True
        raise WrongChannel('You cannot use this cmd outside of bot channels.')

    return commands.check(predicate)


def checkdigitarguments(args, default):
    for item in args:
        if item.isdigit():
            return int(item)
    return default


async def message_handler(message, ctx, time=30, embed=False, delete=True):
    m = await ctx.send(embed=message) if embed else await ctx.send(message)
    if delete:
        await sleep(0)
        await ctx.message.delete()
    await sleep(time)
    await m.delete()


async def message_denied(message, ctx, pm=False):
    await sleep(0)
    await ctx.message.delete()
    m = await ctx.author.send(message) if pm else await ctx.send(message)

    if not pm:
        await sleep(5)
        await m.delete()
