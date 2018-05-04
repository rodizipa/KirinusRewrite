import CONFIG
import discord
import asyncio


async def arole(message):
    parsed_message = message.content.replace(CONFIG.PREFIX + "arole", "")[1:]
    if message.author.id == 114010253938524167:
        parsed_list = parsed_message.split(",")
        new_role = discord.utils.get(message.guild.roles, name=parsed_list[1])
        await message.mentions[0].add_roles(new_role)
        await asyncio.sleep(1)
        await message.delete()
    else:
        await message.author.send("You don't have permissions to do that.")
        await asyncio.sleep(1)
        await message.delete()


async def rrole(message):
    if message.author.id == 114010253938524167:
        parsed_message = message.content.replace(CONFIG.PREFIX + "rrole", "")[1:]
        parsed_list = parsed_message.split(",")
        new_role = discord.utils.get(message.guild.roles, name=parsed_list[1])
        await message.mentions[0].remove_roles(new_role)
        await asyncio.sleep(1)
        await message.delete()
    else:
        await message.author.send("You don't have permissions to do that.")
        await asyncio.sleep(1)
        await message.delete()


async def change_nick(message):
    parsed_message = message.content.replace(CONFIG.PREFIX + "changenick", "")[1:]

    if message.author.id == 114010253938524167:
        list = parsed_message.split(",")
        await message.delete()

        await message.mentions[0].edit(nick=list[1])
    else:
        await message.author.send("You don't have permissions to do that.")
        await message.delete()


async def purge(message):
    if message.author.id == 114010253938524167:
        parsed_message = message.content.replace(CONFIG.PREFIX + "purge", "")[1:]
        await message.delete()
        await message.channel.purge(limit=int(parsed_message))
    else:
        message.author.send("You don't have permissions to do that.")
        await message.delete()