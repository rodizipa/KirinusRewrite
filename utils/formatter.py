from discord import Colour, Embed


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
        em.set_image(url=row["text"])
    else:
        em.description = (row["text"])

    if row['user_id']:

        try:
            member = ctx.guild.get_member(row['user_id'])
        except AttributeError:
            member = ctx.bot.get_user(row['user_id'])
        except:
            pass

        finally:
            member = None

        if member:
            display = member.display_name

            if member.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = member.avatar_url.rsplit("?", 1)[0]
            else:
                avi = member.avatar_url_as(static_format='png')
            em.set_thumbnail(url=avi)
        else:
            display = row['created_by']

        em.add_field(name='Created by', value=display, inline=True)

    elif row['created_by']:
        em.add_field(name='Created by', value=row['created_by'], inline=True)

    if row['created_at']:
        date = row['created_at']
        em.add_field(name='Created at', value=f'{date:%A, %d. %B %Y : %H:%M:%S}', inline=True)

    return em


async def coin_embed(url):
    em = Embed(colour=Colour.dark_blue())
    em.set_image(url=url)

    return em

