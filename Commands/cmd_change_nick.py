import CONFIG

async def ex(message, client):
    parsed_message = message.content.replace(CONFIG.PREFIX + "changenick", "")[1:]

    if message.author.id == 114010253938524167:
        list = parsed_message.split(",")
        await message.delete()

        await message.mentions[0].edit(nick=list[1])
    else:
        await message.author.send("You don't have permissions to do that.")
        await message.delete()
