import random
import CONFIG

# chooses one option


async def ex(message, client):
    if message.channel.id == 167280538695106560 or message.channel.id == 360916876986941442:
        parsed_message = message.content.replace(CONFIG.PREFIX + "choose", "")[1:]
        split_message = parsed_message.split(",")
        await message.channel.send(random.choice(split_message))
    else:
        await message.author.send("This command is locked to `i-am-bot` channel right now.")
        await message.delete()