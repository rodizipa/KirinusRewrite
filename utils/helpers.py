from asyncio import sleep


def checkdigitarguments(args, default):
    for item in args:
        if item.isdigit():
            return int(item)
    return default


async def message_handler(message, ctx, time=30, embed=False, delete=True):
    m = await ctx.send(embed=message) if embed else ctx.send(message)
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
