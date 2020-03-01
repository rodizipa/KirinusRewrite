import asyncio
import logging
from time import gmtime, strftime

import asyncpg
import discord
import pendulum
from discord.ext import commands

import CONFIG
from utils import formatter

logging.basicConfig(level=logging.WARN, filename='error.log')

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=CONFIG.PREFIX, description="Destiny Child KR bot.")
        self.db = kwargs.pop("db")
        self.rt = self.loop.create_task(self.reset_task())

    async def reset_task(self):
        while not self.is_closed():
            now = pendulum.now()

            # Process role time assignment
            role_time = await self.db.fetch("select * from assign_roles")

            for item in role_time:
                server = self.get_guild(int(item['guild_id']))
                member = server.get_member(item['user_id']) if server else None
                check_time = pendulum.instance(item['time'])

                if now > check_time:
                    await self.remove_role_and_dunce(item, member, server)

                else:
                    if member:
                        await self.verify_role(item, member, server)

            await asyncio.sleep(60)

    async def verify_role(self, item, member, server):
        role = discord.utils.get(member.roles, id=item['role_id'])
        if role is None:
            role = discord.utils.get(server.roles, id=item['role_id'])
            await member.add_roles(role)

    async def remove_role_and_dunce(self, item, member, server):
        # remove role (assign plankton if dunce)
        if member:
            role = discord.utils.get(server.roles, id=item['role_id'])
            await member.remove_roles(role)

            if item['role_id'] == 311943704237572097:  # dunce
                # Assign kr role
                kr_role = discord.utils.get(server.roles, id=295083791884615680)
                await member.add_roles(kr_role)

            if item['role_id'] == 506160697323814927:  # NA
                kr_role = discord.utils.get(server.roles, id=295083791884615680)
                await member.add_roles(kr_role)
        # remove row
        connection = await self.db.acquire()
        async with connection.transaction():
            insert = "DELETE FROM assign_roles where user_id = $1;"
            await self.db.execute(insert, item['user_id'])
        await self.db.release(connection)

    async def on_ready(self):
        print(f'{self.user.name} online!')
        print('----')
        await self.change_presence(activity=discord.Game('?help or Die!'))

    async def load_modules(self):
        modules = ['cogs.dbstuff', 'cogs.admin', 'cogs.fun', 'cogs.dc', 'cogs.karma']

        for extension in modules:
            self.load_extension(extension)

    async def on_command_completion(self, ctx):
        print(f'[{strftime("[%d.%m.%Y %H:%M:%S]", gmtime())}] [Command] {ctx.message.content} by {ctx.author.name}')

    async def on_message(self, message):
        if message.content.startswith('?'):
            await self.process_commands(message)
        else:
            try:
                role = discord.utils.get(message.author.roles, id=311943704237572097)
                if role:
                    await formatter.kirinus_gacha(message)

            except discord.DiscordException as ex:
                print("An discord error occurred. Logging.")
                logging.error(ex.__name__, ex)


async def run():

    pg_credentials = {"user": CONFIG.USERNAME, "password": CONFIG.PASSWORD, "database": CONFIG.DATABASE,
                      "host": CONFIG.HOST}
    async with asyncpg.create_pool(**pg_credentials) as db:
        bot = Bot(db=db)
        try:
            bot.remove_command("help")
            await bot.load_modules()
            await bot.start(CONFIG.TOKEN)
        except KeyboardInterrupt:
            await bot.logout()

if __name__ == '__main__':
    print("Starting bot...\n")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except discord.DiscordException as de:
        logging.error(de.__name__)
