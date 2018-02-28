import CONFIG
import csv


async def ex(message, client):
    parsed_message = message.content.replace(CONFIG.PREFIX + "quote", "")[1:]
    with open("Commands/quotes.csv",newline='', encoding='utf-8') as quotes_file:
        reader = csv.DictReader(quotes_file)
        for line in reader:
            if line["invoke"] == parsed_message:
                await message.channel.send(line["text"])