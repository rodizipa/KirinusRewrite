import random

# Gives a random answer

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


async def ex(message, client):
    if message.channel.id == 167280538695106560 or message.channel.id == 360916876986941442:
        await message.channel.send(random.choice(quotes))
    else:
        await message.author.send("My mystical ball only works on channels with rich magic, "
                                                  "like`i-am-bot`.")
        await message.delete()