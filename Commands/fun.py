import random
import CONFIG
from discord import Embed, Color
import asyncio

# Gives a random answer
coinFlip = [
    'https://cdn.discordapp.com/attachments/448341812055244817/448502226021908490/coinsmalltails.png',
    'https://cdn.discordapp.com/attachments/448341812055244817/448502223589212160/coinsmall.png'
]

five_stars = [
    "bastet",
    "mafdet",
    "charles",
    "ashtoreth",
    "cleopatra",
    "hildr",
    "cube_moa",
    "apep",
    "nirrti",
    "aria",
    "sitri",
    "luna",
    "neptune",
    "diablo",
    "dana",
    "horus",
    "maat",
    "venus",
    "elizabeth",
    "kubaba",
    "frey",
    "yan",
    "d_maat",
    "mars",
    "lanfei",
    "rita",
    "pantheon",
    "semele",
    "warwolf",
    "ai",
    "redcross",
    "medusa",
    "metis",
    "hestia",
    "medb",
    "saladin",
    "morgan",
    "tyrfing",
    "demeter",
    "jupiter",
    "hermes",
    "red_queen",
    "verdel",
    "hades",
    "dinashi",
    "aurora",
    "deino",
    "thanatos",
    "eve",
    "bari",
    "d_lisa",
    "saturn",
    "wola",
    "santa",
    "babel",
    "myrina",
    "isolde",
    "naias",
    "sang_ah",
    "willow",
    "anemone",
    "ymir",
    "maris",
    "eshu",
    "rusalka",
    "siren",
    "gd_sang_ah",
    "abaddon",
    "nicole",
    "krampus",
    "jcb",
    "daphnis",
    "midas",
    "ruin",
    "epona",
    "hera",
    "mammon",
    "brownie",
    "newbie_mona",
    "bathory",
    "syrinx",
]

world_bosses = [
    'Aria',
    'Cleo',
    'Apep',
    'Isolde',
    'Khepri',
    'Nicole',
    'Thetis',
    'Demeter',
    'Rita',
    'Slime',
    'Morgan',
    'Krampus',
    'Bari',
]

quotes = [
    'Signs point to yes.',
    'Yes.',
    'Reply hazy, try again.',
    'My sources say no.',
    'You may rely on it.',
    'Concentrate and ask again.',
    'Outlook not so good.',
    'It is decidedly so.',
    'Better not tell you now.',
    'Very doubtful.',
    'Yes - definitely.',
    'It is certain.',
    'Cannot predict now.',
    'Most likely.',
    'Ask again later.',
    'My reply is no.',
    'Outlook good.',
    "Don't count on it."
]

slaps = [
    'slaps {} around a bit with a large trout',
    'gives {} a clout round the head with a fresh copy of WeeChat',
    'slaps {} with a large smelly trout',
    'breaks out the slapping rod and looks sternly at {}',
    'slaps {}\'s bottom and grins cheekily',
    'slaps {} a few times',
    'slaps {} and starts getting carried away',
    'would slap {}, but (s)he is too lazy to do it.',
    'gives {} a hearty slap',
    'finds the closest large object and gives {} a slap with it',
    'likes slapping people and randomly picks {} to slap',
    'dusts off a kitchen towel and slaps it at {}',
    'breaks the 4th wall and slaps {} with the pieces of it.',
    'slaps {} with a b grade stop sign.',
    'slaps {} with a baguette that still freshly baked.'
    'got a whip from chest. Time to try it, {} will be the target.'
]

phrases = [
    'I will not tag people by whim again.',
    'I will donate all my money to Sorrowful.',
    'Ameno.',
]


async def eight_ball(message):
    if message.channel.id == 167280538695106560 or message.channel.id == 360916876986941442:
        await message.channel.send(random.choice(quotes))
    else:
        await message.author.send("My mystical ball only works on channels with rich magic, "
                                  "like`i-am-bot`.")
        await message.delete()


async def choose(message):
    if message.channel.id == 167280538695106560 or message.channel.id == 360916876986941442:
        parsed_message = message.content.replace(CONFIG.PREFIX + "choose", "")[1:]
        split_message = parsed_message.split(",")
        await message.channel.send(random.choice(split_message))
    else:
        await message.author.send("This command is locked to `i-am-bot` channel right now.")
        await message.delete()


async def flip_coin(message):
    em = Embed(color=Color.dark_blue())
    em.set_image(url=random.choice(coinFlip))
    m = await message.channel.send(embed=em)
    await asyncio.sleep(6)
    await message.delete()
    await m.delete()


async def slap(message):
    em = Embed(color=Color.blue(), description="*" + message.author.display_name + " " + random.choice(slaps).format(
        message.mentions[0].display_name) + "*")
    await message.channel.send(embed=em)
    await asyncio.sleep(1)
    await message.delete()


async def replace(message):
    gatcha = random.randint(0, 100)
    if gatcha <= 2:
        await message.delete()
        await asyncio.sleep(1)
        await message.channel.send(random.choice(phrases))


async def gatcha(message):
    if "wb" in message.content.split():
        em = Embed(color=Color.blue(),
                   description=message.author.display_name + " Thinks that the world boss will be " + random.choice(world_bosses))
    else:
        em = Embed(color=Color.blue(), description=message.author.display_name + " guessed " + random.choice(five_stars))
    await message.channel.send(embed=em)
    await asyncio.sleep(1)
    await message.delete()
