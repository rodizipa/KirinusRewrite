import asyncio

# Informs kirinus version


async def ex(message, client):
        await message.channel.send("Kirinus Rewrite")
        await asyncio.sleep(5)
        await message.delete()
