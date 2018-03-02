import CONFIG, datetime
from discord import Embed,Color


async def ex(message, client):
    if message.channel.id == 167280538695106560 or message.channel.id == 397969460297990144 or message.channel.id == 418098311669743637:
        parsed_message = message.content.replace(CONFIG.PREFIX + "raid", "")[1:]
        parsed_list = parsed_message.lower().split(" ")
        m = await message.channel.send("@here")
        author = message.author.display_name
        if len(message.mentions) > 0:
            author = message.mentions[0].display_name

        em = Embed(title="Raid alert!", color = Color.dark_red(), description="@here {} found a raid!".format(author), timestamp=datetime.datetime.utcnow())
        em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418781949465722880/dorrow_cleo.png")

        if parsed_list[0] == 'aria':
            em.color = Color.gold()
            em.title = "Colored Stage!!!"
            em.description = "@here A Wild Aria Appears! Ask {} for the pokeballs".format(author)
            em.set_image(url="https://cdn.discordapp.com/emojis/372407902826135552.png")

        elif parsed_list[0] == 'cleo' or parsed_list[0] == 'cleopatra':
            em.color = Color.gold()
            em.title = "Kneel Before Your Queen"
            em.description = "@here Cleo wants to conquer the city. Join {} and show her that here isn't Egypt.".format(author)
            em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418781949465722880/dorrow_cleo.png")
            
        elif parsed_list[0] == 'slime' or parsed_list[0] == 'pancakes':
            em.color = Color.gold()
            em.title = "Pancakes Wants To Eat The World (Again)"
            em.description = "@here.Pancakes thinks that she is kirby, {} said that she is not. Now we just need judges".format(author)
            em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418594680528437278/something_smaller.png")

        elif parsed_list[0] == 'morgan':
            em.title = "I-It's not like i want to serve you"
            em.description = "@here {} invites you to cafe d'petit. Tsundere maid included.".format(author)
            em.set_image(url="https://cdn.discordapp.com/emojis/372407410192809994.png")

        elif parsed_list[0] == 'rita':
            em.title = "Deus Vult Infidels!"
            em.description= "@here {} was captured by some religious fanatic and will be exorcised. Help him!".format(author)
            em.color = Color.dark_purple()
            em.set_image(url="https://cdn.discordapp.com/emojis/350841507244277764.png")

        elif parsed_list[0] == 'krampus':
            em.title = "Have you been a naughty boy/girl?"
            em.description= "@here Krampus is here searching for bad guys. The funny thing is that u're a devil. Help {} to kick her ass.".format(author)
            em.color = Color.dark_green()
            em.set_image(url="https://cdn.discordapp.com/emojis/280855138044870656.png")

        elif parsed_list[0] == 'frey':
            em.title = "Not him again."
            em.description= "@here {} wants to beat Frey. Motive: It's Frey.".format(author)
            em.color = Color.dark_purple()
            em.set_image(url="https://cdn.discordapp.com/emojis/371474659830661120.png")

        elif parsed_list[0] == 'anemone':
            em.title = "Hey kid, wanna do a bet?"
            em.description= "@here Anemone is trying to gamble with {}. Stop her before she uses your money.".format(author)
            em.color = Color.dark_blue()
            em.set_image(url="https://cdn.discordapp.com/emojis/372015463896449036.png")

        elif parsed_list[0] == 'iseult' or parsed_list[0] == 'isolde':
            em.title = "Warning: Bombs ahead!"
            em.description= "@here {} found a girl with a volleyball shouting **Spiku**. Keep your distance ~~or not~~. U've been warned.".format(author)
            em.color = Color.dark_blue()
            em.set_image(url="https://cdn.discordapp.com/emojis/369336194569601024.png")


        else:
            if len(parsed_list) > 0 and parsed_list[0] != "":
                em.description = "@here {} found a **{}**!".format(author, parsed_list[0])
                if parsed_list[0].startswith("<"):
                    em.description = "@here {} found a raid!".format(author)
                    
        if len(parsed_list) > 1 :
            if not parsed_list[1].startswith("<"):
                em_edit = em.description
                em.description = em_edit + "\nAlso, it appears to be lvl **{}**.\n".format(parsed_list[1])

        await m.delete()
        await message.channel.send(embed=em)
        await message.delete()
    else:
        await message.delete()
        await message.author.send("Don't do raid calls outside of raid channel.")

