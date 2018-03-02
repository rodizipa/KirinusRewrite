import CONFIG
import csv
from discord import Embed, Color

#description = "Search Child Info on Database"

async def ex(message, client):
    if message.channel.id == 167280538695106560 or message.channel.id == 360916876986941442:
        async with open("Commands/kdbchilds.csv", "r") as db_childs_file:
            reader = csv.DictReader(db_childs_file)

            # if the keyword was found
            found = False
            #filtered word
            qchild = message.content.replace(CONFIG.PREFIX + "child", "")[1:]

            for line in reader:
                if (line["id"] == qchild.lower()) or (line["alias1"]== qchild.lower()) or (line["alias2"] == qchild.lower()):
                    found = True
                    #Chooses the element color
                    if line["element"] == "Light":
                        element_color = Color.gold()
                    elif line["element"] == "Dark":
                        element_color = Color.dark_purple()
                    elif line["element"] == "Fire":
                        element_color = Color.dark_red()
                    elif line["element"] == "Water":
                        element_color = Color.dark_blue()
                    elif line["element"] == "Forest":
                        element_color = Color.dark_green()

                    #creates the embed card
                    embed = Embed(color = element_color, description=line["rank"])
                    embed.title = line["Name"]
                    embed.add_field(name="Type:", value=line["type"] + "\n", inline=True)
                    embed.add_field(name="Element", value=line["element"]+ "\n", inline=True)
                    embed.add_field(name="Leader Skill", value=line["Leader"]+ "\n", inline=False)
                    embed.add_field(name="Auto Skill", value=line["Auto"]+ "\n", inline=False)
                    embed.add_field(name="Tap Skill", value=line["Tap"]+ "\n", inline=False)
                    embed.add_field(name="Slide Skill", value=line["Slide"]+ "\n",inline=False)
                    embed.add_field(name="Drive Skill", value=line["Drive"]+ "\n", inline=False)
                    embed.set_footer(text=line["notes"], icon_url="https://i.imgur.com/zcJGvMI.png")
                    embed.set_thumbnail(url=line["thumbnail"])
                    embed.set_image(url=line["image"])

                    await message.channel.send(embed=embed)
                    break

            if found is False:
                    embed = Embed(color = Color.dark_grey(), description="Child Not Found >.<")
                    embed.set_image(url="https://i.imgur.com/cf1TReg.jpg")
                    await message.channel.send(embed=embed)
                    with open("aliasesresearch.txt", "a") as aliases_research_file:
                        aliases_research_file.write(qchild + ",")

    else:
        await message.delete()
        await message.author.send("I see that u tried to search a child outside of the `i-am-bot` channel, "
                                                  "so i'll ignore you.")