import CONFIG, datetime
from discord import Embed, Color


async def ex(message, client):
    if message.channel.id == 167280538695106560 or message.channel.id == 423263557828739073:
        parsed_message = message.content.replace(CONFIG.PREFIX + "raid", "")[1:]
        parsed_list = parsed_message.lower().split(" ")
        m = await message.channel.send("@here")
        author = message.author.display_name

        if len(message.mentions) > 0:
            author = message.mentions[0].display_name

        em = Embed(title="Raid alert!", color=Color.dark_red(), description="@here {} found a raid!".format(author),
                   timestamp=datetime.datetime.utcnow())
        em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418781949465722880/dorrow_cleo.png")

        if parsed_list[0] == 'aria':
            em.color = Color.gold()
            em.title = "Colored Stage!!!"
            em.description = "@here A Wild Aria Appears! Ask {} for the pokeballs".format(author)
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438159951986708/Aria.png")

        elif parsed_list[0] == 'cleo' or parsed_list[0] == 'cleopatra':
            em.color = Color.gold()
            em.title = "Kneel Before Your Queen"
            em.description = "@here Cleo wants to conquer the city. Join {} and show her that here isn't Egypt.".format(
                author)
            em.set_image(
                url="https://cdn.discordapp.com/attachments/242845451739463681/418781949465722880/dorrow_cleo.png")
            for item in parsed_list:
                if item == 'slayers' or item == 'slayer':
                    em.set_image(
                        url="https://cdn.discordapp.com/attachments/167280538695106560/420924635459092480/slayerscleo.png")

        elif parsed_list[0] == 'slayer' or parsed_list[0] == 'slayers':
            em.set_image(url='https://cdn.discordapp.com/attachments/167280538695106560/420924635459092480/slayerscleo.png')

        elif parsed_list[0] == 'slime' or parsed_list[0] == 'pancakes':
            em.color = Color.gold()
            em.title = "Pancakes Wants To Eat The World (Again)"
            em.description = "@here.Pancakes thinks that she is kirby, {} said that she is not. Now we just need judges".format(
                author)
            em.set_image(
                url="https://cdn.discordapp.com/attachments/242845451739463681/418594680528437278/something_smaller.png")
            for item in parsed_list:
                if item == 'slayers' or item == 'slayer':
                    em.set_image(
                        url="https://cdn.discordapp.com/attachments/167280538695106560/420925799491698688/slayersslime.png")


        elif parsed_list[0] == 'morgan':
            em.title = "I-It's not like i want to serve you"
            em.description = "@here {} invites you to cafe d'petit. Tsundere maid included.".format(author)
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438370388475914/morgan.png")

        elif parsed_list[0] == 'rita':
            em.title = "Deus Vult Infidels!"
            em.description = "@here {} was captured by some religious fanatic and will be exorcised. Help him!".format(
                author)
            em.color = Color.dark_purple()
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438469042831370/rita.png")

        elif parsed_list[0] == 'krampus':
            em.title = "Have you been a naughty boy/girl?"
            em.description = "@here Krampus is here searching for bad guys. The funny thing is that u're a devil. Help {} to kick her ass.".format(
                author)
            em.color = Color.dark_green()
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438405054529537/krampus.png")

        elif parsed_list[0] == 'frey':
            em.title = "Not him again."
            em.description = "@here {} wants to beat Frey. Motive: It's Frey.".format(author)
            em.color = Color.dark_purple()
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438459756642305/Frey.png")

        elif parsed_list[0] == 'anemone':
            em.title = "Hey kid, wanna do a bet?"
            em.description = "@here Anemone is trying to gamble with {}. Stop her before she uses your money.".format(
                author)
            em.color = Color.dark_blue()
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438523338096640/anemone.png")

        elif parsed_list[0] == 'iseult' or parsed_list[0] == 'isolde':
            em.title = "Warning: Bombs ahead!"
            em.description = "@here {} found a girl with a volleyball shouting **Spiku**. Keep your distance ~~or not~~. U've been warned.".format(
                author)
            em.color = Color.dark_blue()
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438528870383616/isolde.png")

        elif parsed_list[0] == 'verd' or parsed_list[0] == 'verdel':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438373009915924/verd.png")

        elif parsed_list[0] == 'mars':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438164578304015/Mars.png")
            em.color = Color.dark_purple()

        elif parsed_list[0] == 'neptune':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438171058372628/Neptune.png")
            em.color = Color.dark_gold()

        elif parsed_list[0] == 'saturn':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438173985996810/Saturn.png")
            em.color = Color.dark_blue()

        elif parsed_list[0] == 'bari':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438224753852416/bari.png")
            em.color = Color.dark_blue()

        elif parsed_list[0] == 'santa':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438412893552640/santa.png")
            em.color = Color.dark_blue()

        elif parsed_list[0] == 'willow' or parsed_list[0] =='barchelor':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438249588326400/willow.png")
            em.color = Color.dark_green()

        elif parsed_list[0] == 'tristan':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438531726573569/tristan.png")
            em.color = Color.dark_green()

        elif parsed_list[0] == 'apep':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438292902903851/apep.png")
            em.color = Color.dark_gold()

        elif parsed_list[0] == 'bast':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438297613369354/bastet.png")
            em.color = Color.dark_gold()

        elif parsed_list[0] == 'horus':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438314176413696/horus.png")
            em.color = Color.dark_gold()

        elif parsed_list[0] == 'hildr' or parsed_list[0] == 'hilde':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438365216899085/hildr.png")
            em.color = Color.dark_gold()

        elif parsed_list[0] == 'neman':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438463892226068/Neman.png")
            em.color = Color.dark_purple()

        elif parsed_list[0] == 'nicole':
            em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())
            em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438410498736148/nicole.png")
            em.color = Color.dark_green()

        elif parsed_list[0]:
            if parsed_list[0] == message.mentions[0]:
                em.description = "@here {} found a raid.".format(author)
            else:
                em.description = "@here {} found a **{}**".format(author, parsed_list[0].capitalize())


        if len(parsed_list) > 1:
            found = False
            for item in parsed_list:
                if item.isdigit():
                    level = item
                    found = True
                    break
            if found:
                em_edit = em.description
                em.description = em_edit + "\nAlso, it appears to be lvl **{}**.\n".format(level)

        await m.delete()
        await message.channel.send(embed=em)
        await message.delete()
    else:
        await message.delete()
        await message.author.send("Don't do raid calls outside of raid channel.")
