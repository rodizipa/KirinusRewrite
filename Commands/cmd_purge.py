import CONFIG
target = None


async def is_target(m):
    return m.author.mention == target


async def ex(message, client):
    if message.author.id == 114010253938524167:
        parsed_message = message.content.replace(CONFIG.PREFIX + "purge", "")[1:]
        await message.delete()
        if parsed_message.startswith('<@'):
            p_list = parsed_message.split(" ")
            target = p_list[0]
            await message.channel.purge(limit=int(p_list[1]), check=is_target(target))
        else:
            await message.channel.purge(limit=int(parsed_message))
    else:
        message.author.send("You don't have permissions to do that.")
        await message.delete()