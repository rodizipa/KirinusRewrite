import random
import CONFIG
from discord import Embed, Color
import asyncio

# Gives a random answer
coinFlip=[
    'https://cdn.discordapp.com/attachments/448341812055244817/448342010638893056/tailssmall.png',
    'https://cdn.discordapp.com/attachments/448341812055244817/448342048173719573/headssmall.png'
]

quotes=[
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
    'would slap {}, but he is too lazy to do it.',
    'gives {} a hearty slap',
    'finds the closest large object and gives {} a slap with it',
    'likes slapping people and randomly picks {} to slap',
    'dusts off a kitchen towel and slaps it at {}',
    'breaks the 4th wall and slaps {} with the pieces of it.',
    'slaps {} with a b grade stop sign.',
    'slaps {} with a baguette that still freshly baked.'
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
    await asyncio.sleep(20)
    await message.delete()
    await m.delete()


async def slap(message):
    await message.channel.send("*"+ message.author.mention + " " + random.choice(slaps).format(message.mentions[0].mention)+"*")
    await asyncio.sleep(1)
    await message.delete()