import discord
import asyncio
from time import gmtime, strftime
import CONFIG


wb_status = False
wb_first_call = False


#importing commands
from Commands import cmd_search_child, cmd_help, cmd_version, cmd_8ball, cmd_choose, cmd_quote, cmd_say, cmd_purge,\
    cmd_change_nick,cmd_raidcall, cmd_emoji, cmd_assign_role


cmdmap = {
    "child": cmd_search_child,
    "help": cmd_help,
    "version": cmd_version,
    "8ball": cmd_8ball,
    "choose": cmd_choose,
    "quote": cmd_quote,
    "say": cmd_say,
    "purge": cmd_purge,
    "changenick": cmd_change_nick,
    "raid": cmd_raidcall,
    "emo": cmd_emoji,
    "arole" :cmd_assign_role,
}


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.world_boss_task())

    async def on_ready(self):
        print(self.user.name + " online!")
        print(self.user.id)
        print('------')

        await self.change_presence(game=discord.Game(name='?help or Die!'))

    async def  world_boss_task(self):
        await self.wait_until_ready()
        global wb_status
        global wb_first_call
        wb_channel = self.get_channel(423263557828739073) # general channel to catch the guild

        while not self.is_closed():
            while wb_status is True:
                if wb_first_call is True:
                    await wb_channel.send("@here World Boss Started!!!")
                    wb_first_call = False
                    await asyncio.sleep(7200)
                else:
                    await wb_channel.send("@here ticket reset!")
                    await asyncio.sleep(7200)

            await asyncio.sleep(1) #1s

    async def on_message(self, message):

        if message.content.startswith('?wb'):
            parsed_message = message.content.replace("?wb", "")[1:]
            global wb_first_call
            global wb_status
            if parsed_message == "start":
                wb_status = True
                wb_first_call = True
            elif parsed_message == "stop":
                wb_status = False
                message.channel.send("@here World Boss is Dead.")
            await message.delete()

        elif message.content.startswith(CONFIG.PREFIX) and not message.author == client.user:
            invoke = message.content.split(" ")[0].replace(CONFIG.PREFIX, "", 1)
            command_string =""
            cmd = cmdmap[invoke]

            try:
                await cmd.ex(message, client)
            except Exception as e:
                print(e.__doc__)
                print(e.__name__)

            print(strftime("[%d.%m.%Y %H:%M:%S]",
                           gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)


client = MyClient()
client.run(CONFIG.TOKEN)