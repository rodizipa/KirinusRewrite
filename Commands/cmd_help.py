from discord import Embed, Color

#description = "Help"

async def ex(message, client):
    await message.author.send( embed=Embed(
        color=Color.purple(),
        title="Lost? Don't Worry, Kirinus is here!\n",
        description="I'll help you in this adventure! Know that commands doesn't ignore case like childs ID.\n\n**?help:** Shows"
                    " this screen\n\n **Commands List**:https://rodizipa.github.io/KirinusRewrite/"
        ).set_image(url="https://i.imgur.com/vqF3d4O.png"))
    await message.delete()