from discord import Colour, Embed
import datetime
import random


async def element_color(element):
    switch = {
        'Light': Colour.gold(),
        'Dark': Colour.dark_purple(),
        'Fire': Colour.dark_red(),
        'Water': Colour.dark_blue(),
        'Forest': Colour.dark_green()
    }
    return switch.get(element)


async def child_embed(row):
    em = Embed(color=await element_color(row["element"]), description=row["rank"])
    em.title = row["name"]
    em.add_field(name="Role", value=row["role"], inline=True)
    em.add_field(name="Element", value=row["element"], inline=True)
    em.add_field(name="Leader Skill", value=row["leader_skill"], inline=False)
    em.add_field(name="Auto Skill", value=row["auto_skill"], inline=False)
    em.add_field(name="Tap Skill", value=row["tap_skill"], inline=False)
    em.add_field(name="Slide Skill", value=row["slide_skill"], inline=False)
    em.add_field(name="Drive Skill", value=row["drive_skill"], inline=False)
    if row["notes"] is not None:
        em.set_footer(text=row["notes"], icon_url="https://i.imgur.com/zcJGvMI.png")
    if row["thumbnail"] is not None:
        em.set_thumbnail(url=row["thumbnail"])
    if row["image"] is not None:
        em.set_image(url=row["image"])

    return em


async def quote_embed(row):
    em = Embed(title=row['invoke'], color=Colour.dark_blue())

    if row['text'].startswith("http") or row['text'].startswith(" http"):
        em.set_image(url=row["text"])
    else:
        em.description = (row["text"])

    return em


async def quote_info(ctx, row):
    em = Embed(title=row['invoke'], color=Colour.dark_blue())

    if row['text'].startswith("http") or row['text'].startswith(" http"):
        em.set_thumbnail(url=row["text"])
    else:
        em.description = (row["text"])

    if row['user_id']:

        member = ctx.guild.get_member(row['user_id'])
        
        if member:
            display = member.display_name
            em.set_author(name='Tag info', icon_url=member.avatar_url)
        else:
            display = row['created_by']

        em.add_field(name='Created by', value=display, inline=True)

    elif row['created_by']:
        em.add_field(name='Created by', value=row['created_by'], inline=True)

    if row['created_at']:
        date = row['created_at']
        em.add_field(name='Created at', value=f'{date:%d. %B %Y : %H:%M:%S}', inline=True)

    return em


async def coin_embed(url):
    em = Embed(colour=Colour.dark_blue())
    em.set_image(url=url)

    return em


async def wb_ticket_reset():
    em = Embed(title="Ticket Reset!", description=':alarm_clock: @here Ticket reset! :alarm_clock:', timestamp=datetime.datetime.utcnow())
    return em


gacha_phrases = [
    'Ameno.',
    "I'll not do this again.",
    "Don't mind me, i'm a dunce.",
    "Get cucked bro.",
    "Not on my duty.",
    "Oof",
]


async def kirinus_gacha(message):
    if random.randrange(1, 100) < 5:
        await message.delete()
        await message.channel.send(random.choice(gacha_phrases))
    else:
        return None
