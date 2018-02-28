import CONFIG
import asyncio

# repeats the phrase for some reason (like testing)


async def ex(message, client):
    parsed_message = message.content.replace(CONFIG.PREFIX + "say", "")[1:]
    await message.channel.send(parsed_message)
    await asyncio.sleep(5)
    await message.delete()