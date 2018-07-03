import pendulum
import asyncio
from discord import Embed, Color
import CONFIG
import shlex


async def reset(message):
    now = pendulum.now('Asia/Seoul')
    if now.hour > 3:
        quest_reset = now.tomorrow('Asia/Seoul').add(hours=4)
    else:
        quest_reset = pendulum.today('Asia/Seoul').add(hours=4)

    reset_countdown = quest_reset.diff(now)

    em = Embed(description=":alarm_clock: The next reset will happen in {}. :alarm_clock:".format(reset_countdown),
               color=Color.blue())

    m = await message.channel.send(embed=em)
    await asyncio.sleep(20)
    await message.delete()
    await m.delete()


async def maint(message):
    global game_time
    parsed_message = message.content.replace(CONFIG.PREFIX + "maint", "")[1:]
    parsed_list = shlex.split(parsed_message)

    if len(parsed_list) == 0:
        with open('Commands/maint.txt', 'r') as maint_file:
            for line in maint_file:
                game_time = pendulum.parse(line)
            now = pendulum.now('Asia/Seoul')

            if now > game_time:
                em = Embed(description=":alarm_clock: Maint started {} ago. :alarm_clock:".format(game_time.diff(now)),
                           color=Color.blue())
                m = await message.channel.send(embed=em)
                await asyncio.sleep(20)
                await message.delete()
                await m.delete()
            else:
                em = Embed(description=":alarm_clock: Maint will start in {}. :alarm_clock:".format(game_time.diff(now)),
                           color=Color.blue())
                m = await message.channel.send(embed=em)
                await asyncio.sleep(20)
                await message.delete()
                await m.delete()

    elif parsed_list[0] == "add":
        if message.author.id == 224522663626801152 or message.author.id == 114010253938524167:
            game_time = pendulum.parse(parsed_list[1], tz="Asia/Seoul")
            strparse = str(game_time)

            with open("Commands/maint.txt", 'w') as maint_file:
                maint_file.write(strparse)

            m = await message.channel.send("Maint updated!")
            await asyncio.sleep(5)
            await message.delete()
            await m.delete()
        else:
            m = await message.channel.send("You don't have permissions to do that!")
            await asyncio.sleep(5)
            await message.delete()
            await m.delete()


async def timer(message):
    parsed_message = message.content.replace(CONFIG.PREFIX + "timer", "")[1:]
    countdown = pendulum.parse(parsed_message, tz='Asia/Seoul')
    now = pendulum.now('Asia/Seoul')

    if now > countdown:
        em = Embed(description=":alarm_clock: This event happened {} ago. :alarm_clock:".format(countdown.diff(now)),
                   color=Color.blue())
        m = await message.channel.send(embed=em)
        await asyncio.sleep(20)
        await message.delete()
        await m.delete()
    else:
        em = Embed(description=":alarm_clock: This event will happen in {}. :alarm_clock:".format(countdown.diff(now)),
                   color=Color.blue())
        m = await message.channel.send(embed=em)
        await asyncio.sleep(20)
        await message.delete()
        await m.delete()
