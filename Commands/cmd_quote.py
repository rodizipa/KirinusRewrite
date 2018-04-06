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
        wrapper_list=[]
        counter = 0

        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                if counter <= 1:
                    tag_list.append(line["invoke"])
                    counter += 1
                elif counter == 2:
                    tag_list.append(line["invoke"])
                    counter = 0
                    wrapper_list.append(', '.join(str(tag) for tag in tag_list))
                    tag_list.clear()
            if tag_list:
                wrapper_list.append(', '.join(str(tag) for tag in tag_list))

            makestring = ',\n'.join(line for line in wrapper_list)
            em = Embed(title="Current Tags:", description=makestring)
            await message.author.send(embed = em)

        await message.delete()

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