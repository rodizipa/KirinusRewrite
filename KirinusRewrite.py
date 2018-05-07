import discord
import asyncio
from time import gmtime, strftime
import CONFIG

from Commands import db, utils, fun, meme, raid, admin, timer

cmd_map = {
    "child": db.child_search,
    "help": utils.help,
    "8ball": fun.eight_ball,
    "choose": fun.choose,
    "quote": meme.quote,
    "say": utils.say,
    "purge": admin.purge,
    "changenick": admin.change_nick,
    "raid": raid.raid,
    "emo": meme.emoji,
    "arole": admin.arole,
    "reset": timer.reset,
    "maint": timer.maint,
    "rrole": admin.rrole,
    "timer": timer.timer,
    "tierlist": utils.tierlist,
}


class WorldBoss:
    status = False
    channel = None
    first_run = False
    reset_time = 7200  # actual time: 2h


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the world_boss task and run it in the background
        self.bg_task = self.loop.create_task(self.world_boss_task())

    async def on_ready(self):
        print(self.user.name + " online!")
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Game('?help or Die!'))

    async def world_boss_task(self):
        await self.wait_until_ready()
        # WorldBoss.channel = self.get_channel(423263557828739073)
        WorldBoss.channel = self.get_channel(167280538695106560)

        while not self.is_closed():
            while WorldBoss.status is True:
                if WorldBoss.first_run is True:
                    WorldBoss.first_run = False
                    await asyncio.sleep(WorldBoss.reset_time)
                else:
                    m = await WorldBoss.channel.send("@here Ticket reset!")
                    await m.delete()
                    await WorldBoss.channel.send(embed = raid.wb_ticket())
                    await asyncio.sleep(WorldBoss.reset_time)
            await asyncio.sleep(1)  # 1s

    async def on_message(self, message):

        if message.content.startswith('?wb') and not message.author == client.user:
            parsed_message = message.content.replace("?wb", "")[1:]
            parsed_message = parsed_message.lower().split()

            if parsed_message[0] == "start":
                WorldBoss.first_run = True
                WorldBoss.status = True

                if len(parsed_message) > 1:
                    m = await WorldBoss.channel.send("@here World Boss started! {}".format(parsed_message[1]))
                    await m.delete()
                    await WorldBoss.channel.send(embed=raid.wb_card(parsed_message[1]))
                else:
                    m = await WorldBoss.channel.send("@here World Boss started!")
                    await m.delete()
                    await WorldBoss.channel.send(embed=raid.wb_card("default"))

            elif parsed_message[0] == "stop":
                m = await WorldBoss.channel.send("@here World Boss died")
                await m.delete()
                await WorldBoss.channel.send(embed= raid.wb_died())
                WorldBoss.status = False

            await asyncio.sleep(1)
            await message.delete()

        elif message.content.startswith(CONFIG.PREFIX) and not message.author == client.user:
            invoke = message.content.split(" ")[0].replace(CONFIG.PREFIX, "", 1)
            cmd = cmd_map[invoke]

            try:
                await cmd(message)
            except Exception as e:
                print(e.__name__)
                print(e.__doc__)

            print(strftime("[%d.%m.%Y %H:%M:%S]",
                           gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)


client = MyClient()
client.run(CONFIG.TOKEN)