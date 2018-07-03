import CONFIG
import csv
from discord import Embed, Color
import asyncio
import shlex


# melhorias: 2nd page listing,listing creator nick.


async def quote(message):
    global m
    parsed_message = message.content.replace(CONFIG.PREFIX + "quote", "")[1:]
    parsed_list = shlex.split(parsed_message)

    # list tags

    if len(parsed_list) == 0 or parsed_list[0] in ('list', 'help'):
        tag_list = []
        wrapper_list = []
        counter = 0

        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                if counter <= 3:
                    tag_list.append(line["invoke"])
                    counter += 1
                elif counter == 4:
                    tag_list.append(line["invoke"])
                    counter = 0
                    wrapper_list.append(', '.join(str(tag) for tag in tag_list))
                    tag_list.clear()
            if tag_list:
                wrapper_list.append(', '.join(str(tag) for tag in tag_list))

            makestring = ',\n'.join(line for line in wrapper_list)
            em = Embed(title="Current Tags:", description=makestring)
            await message.author.send(embed=em)

        await message.delete()

    # add item
    elif parsed_list[0] == "add":
        found = False
        line_list = []
        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                if line["invoke"] == parsed_list[1]:
                    found = True
                    line_list.append("{},{}".format(line["invoke"], parsed_list[2]))
                else:
                    line_list.append("{},{}".format(line["invoke"], line["text"]))

        if found:
            with open("Commands/quotes.csv", 'w', encoding='utf-8') as quotes_file:
                quotes_file.write("invoke,text\n")
                for line in line_list:
                    quotes_file.write(line + '\n')
            m = await message.channel.send("Tag updated.")

        if not found:
            with open("Commands/quotes.csv", "a") as quotes_file:
                quotes_file.write('\n{},{}'.format(parsed_list[1], parsed_list[2]))
            m = await message.channel.send("Tag added.")

        await asyncio.sleep(5)
        await m.delete()
        await message.delete()

    # remove item
    elif parsed_list[0] == "remove":
        line_list = []
        found = False

        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)
            for line in reader:
                if line["invoke"] == parsed_list[1]:
                    found = True
                    break
                else:
                    line_list.append("{},{}".format(line["invoke"], line["text"]))

        if found:
            with open("Commands/quotes.csv", 'w', encoding='utf-8') as quotes_file:
                quotes_file.write("invoke,text\n")
                for line in line_list:
                    quotes_file.write(line + '\n')

            m = await message.channel.send("Tag removed.")
        else:
            m = await message.channel.send("Tag not found.")

        await asyncio.sleep(5)
        await m.delete()
        await message.delete()

    # find item
    else:
        with open("Commands/quotes.csv", newline='', encoding='utf-8') as quotes_file:
            reader = csv.DictReader(quotes_file)

            found = False

            for line in reader:
                if line["invoke"] == parsed_list[0]:
                    if line["text"].startswith("http") or line["text"].startswith(" http"):
                        em = Embed(title=line["invoke"], color=Color.dark_blue())
                        em.set_image(url=line["text"])
                        em.set_footer(text="Invoked by: " + message.author.display_name)
                        await message.channel.send(embed=em)
                        await message.delete()
                    else:
                        await message.channel.send(line["text"])
                    found = True
                    break

            if not found:
                m = await message.channel.send("Tag not found.")
                await asyncio.sleep(5)
                await m.delete()
                await message.delete()


async def emoji(message):
    if message.author.id == 114010253938524167:
        parsed_message = message.content.replace(CONFIG.PREFIX + "emo", "")[1:]
        with open("Commands/emotes.csv", newline='', encoding='utf-8') as emotes_file:
            reader = csv.DictReader(emotes_file)

            for item in reader:
                if item["invoke"] == parsed_message:
                    await message.delete()
                    await message.channel.send(item["id"])
                    break
