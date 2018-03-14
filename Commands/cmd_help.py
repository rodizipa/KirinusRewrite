from discord import Embed, Color

#description = "Help"

async def ex(message, client):
    await message.author.send( embed=Embed(
        color=Color.purple(),
        title="Lost? Don't Worry, Kirinus is here!\n",
        description="I'll help you in this adventure! Know that commands doesn't ignore case like childs ID.\n\n**?help:** Shows"
                    " this screen\n\n**?version:** Show my version\n\n"
                    "**?8ball <phrase>:** Ask the mystical ball and it will answer.\n\n"
                    "**?choose <term1>, <term2>[, <term whatever>].** Chooses a option for you. Note that terms are separated by commas\n\n"
                    "**?child <name>:** I'll search the child on my database (Child name ignores case, names with space needs "
                    "to keep the space. Ex:?child sang ah.\n\n"
                    "**?raid read the doc: https://rodizipa.github.io/KirinusRewrite/"
        ).set_image(url="https://i.imgur.com/vqF3d4O.png"))
    await message.delete()