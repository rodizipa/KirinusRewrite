import discord
import asyncio
from time import gmtime, strftime
import CONFIG


perma_name = False


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
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(self.user.name + " online!")
        print(self.user.id)
        print('------')

        await self.change_presence(game=discord.Game(name='?help or Die!'))

    async def my_background_task(self):
        await self.wait_until_ready()
        global perma_name
        channel = self.get_channel(242845451739463681) # general channel to catch the guild
        perma_user = channel.guild.get_member(202591264510574592) #user id koji
        perma_new_name = "Failure 2.0"
        perma_user2 = channel.guild.get_member(186869907898499074) #blake

        while not self.is_closed():
            while perma_name is True:
                if perma_user.display_name is not perma_new_name:
                    await perma_user.edit(nick=perma_new_name) #permanick
                if perma_user2.display_name is not "Koji 2.0":
                    await perma_user2.edit(nick="Koji 2.0")
            await asyncio.sleep(5) # task runs every 5 seconds

    async def on_message(self, message):

        if message.content.startswith('?permaname'):
            if message.author.id == 114010253938524167:
                parsed_message = message.content.replace("?permaname", "")[1:]
                global perma_name
                if parsed_message == "True":
                    perma_name = True
                elif parsed_message == "False":
                    perma_name = False
            await asyncio.sleep(3)
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