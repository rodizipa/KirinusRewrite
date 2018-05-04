from discord import Embed, Color
import asyncio
import CONFIG


async def help(message):
    await message.author.send( embed=Embed(
        color=Color.purple(),
        title="Lost? Don't Worry, Kirinus is here!\n",
        description="I'll help you in this adventure! Know that commands doesn't ignore case like childs ID.\n\n**?help:** Shows"
                    " this screen\n\n **Commands List**:https://rodizipa.github.io/KirinusRewrite/"
        ).set_image(url="https://i.imgur.com/vqF3d4O.png"))
    await asyncio.sleep(1)
    await message.delete()


async def say(message):
    parsed_message = message.content.replace(CONFIG.PREFIX + "say", "")[1:]
    await message.channel.send(parsed_message)
    await asyncio.sleep(5)
    await message.delete()