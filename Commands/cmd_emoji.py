import CONFIG
import csv


async def ex(message, client):
    if message.author.id == 114010253938524167:
        parsed_message = message.content.replace(CONFIG.PREFIX + "emo", "")[1:]
        with open("Commands/emotes.csv", newline='', encoding='utf-8') as emotes_file:
            reader = csv.DictReader(emotes_file)

            for emoji in reader:
                if emoji["invoke"] == parsed_message:
                    await message.delete()
                    await message.channel.send(emoji["id"])

