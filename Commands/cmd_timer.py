import pendulum
import asyncio
from discord import Embed, Color

async def ex(message, client):
    now = pendulum.now('Asia/Seoul')
    if (now.hour > 3):
        reset = now.tomorrow('Asia/Seoul').add(hours=4)
    else:
        reset = pendulum.today('Asia/Seoul').add(hours=4)

    reset_countdown = reset.diff(now)

    em = Embed(description=":alarm_clock: The next reset will happen in {}. :alarm_clock:".format(reset_countdown), color=Color.blue())
    await asyncio.sleep(1)
    await message.delete()
    m = await message.channel.send(embed = em)
    await asyncio.sleep(20)
    await m.delete()
