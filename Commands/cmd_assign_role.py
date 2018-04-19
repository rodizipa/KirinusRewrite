import CONFIG
import discord


async def ex(message, client):
    parsed_message = message.content.replace(CONFIG.PREFIX + "arole", "")[1:]
    if message.author.id == 114010253938524167:
        list = parsed_message.split(",")
        if len(list) >2:
            if list[2]=="remove":
                user_roles = message.mentions[0].roles[:]
                new_role = discord.utils.get(message.guild.roles, name=list[1])
                await message.mentions[0].remove_roles(new_role)
        else:
            user_roles = message.mentions[0].roles[:]
            new_role = discord.utils.get(message.guild.roles, name=list[1])
            await message.mentions[0].add_roles(new_role)
            await message.delete()
    else:
        await message.author.send("You don't have permissions to do that.")
        await message.delete()
