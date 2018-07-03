import CONFIG
import csv
from discord import Embed, Color

# description = "Search Child Info on Database"


async def child_search(message):
    if message.channel.id in (167280538695106560, 360916876986941442, 378255860377452545, 458755509890056222):
        with open("Commands/kdbchilds.csv", "r") as db_childs_file:
            reader = csv.DictReader(db_childs_file)

            # if the keyword was found
            found = False
            # filtered word
            qchild = message.content.lower().replace(CONFIG.PREFIX + "child", "")[1:]

            for line in reader:
                if qchild in (line["child_call"], line["alias1"],line["alias2"]):
                    found = True
                    # Chooses the element color
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

                    # creates the embed card
                    embed = Embed(color=element_color, description=line["rank"])
                    embed.title = line["name"]
                    embed.add_field(name="Type:", value=line["role"] + "\n", inline=True)
                    embed.add_field(name="Element", value=line["element"]+ "\n", inline=True)
                    embed.add_field(name="Leader Skill", value=line["leader_skill"]+ "\n", inline=False)
                    embed.add_field(name="Auto Skill", value=line["auto_skill"]+ "\n", inline=False)
                    embed.add_field(name="Tap Skill", value=line["tap_skill"]+ "\n", inline=False)
                    embed.add_field(name="Slide Skill", value=line["slide_skill"]+ "\n",inline=False)
                    embed.add_field(name="Drive Skill", value=line["drive_skill"]+ "\n", inline=False)
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
