import CONFIG
import csv
from discord import Embed
import asyncio
import shlex

async def ex(message, client):
    parsed_message = message.content.replace(CONFIG.PREFIX + "quote", "")[1:]
    parsed_list = shlex.split(parsed_message)

# list tags

    if len(parsed_list) == 0 or parsed_list[0] == "help" or parsed_list[0] == "list":
        tag_list =[]

        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                tag_list.append(line["invoke"])

            makestring = ' \n'.join(str(tag) for tag in tag_list)
            em = Embed(title="Page 1/1", description=makestring)
            await message.author.send(embed = em)

        message.delete()

# add item
    elif parsed_list[0] == "add":
        found = False
        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                if line["invoke"] == parsed_list[1]:
                    await message.channel.send("Row Replacement not yet implemented.")
                    found = True
        if not found:
            with open("Commands/quotes.csv", "a") as quotes_file:
                quotes_file.write('\n{}, {}'.format(parsed_list[1], parsed_list[2]))

            m = await message.channel.send("Tag added.")
            await asyncio.sleep(5)
            await m.delete()

# find item
    else:
        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)

            found = False

            for line in reader:
                if line["invoke"] == parsed_list[0]:
                    await message.channel.send(line["text"])
                    found = True
                    break

            if not found:
                m = await message.channel.send("Tag not found.")
                await asyncio.sleep(5)
                await m.delete()