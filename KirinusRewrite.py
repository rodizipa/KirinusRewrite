import discord
from discord.ext import commands
import asyncio
import asyncpg
from time import gmtime, strftime
from utils import formatter
import CONFIG
import pendulum


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=CONFIG.PREFIX, description="Destiny Child KR bot.")
        self.db = kwargs.pop("db")
        self.rt = self.loop.create_task(self.reset_task())

    async def reset_task(self):
        await self.wait_until_ready()
        claim_reset = None
        rolls_reset = None
        decay_affinity = None

        while not self.is_closed():
            query = "select * from alarms"
            rows = await self.db.fetch(query)

            for item in rows:
                if item['alarm_name'] == 'claim_reset':
                    claim_reset = pendulum.instance(item['alarm_time'])
                elif item['alarm_name'] == 'rolls_reset':
                    rolls_reset = pendulum.instance(item['alarm_time'])
                elif item['alarm_name'] == 'decay_affinity':
                    decay_affinity = pendulum.instance(item['alarm_time'])

            now = pendulum.now()

            if now > claim_reset:
                claim_reset = claim_reset.add(hours=6)
                claim_reset = formatter.pendulum_to_datetime(claim_reset)

                connection = await self.db.acquire()
                async with connection.transaction():
                    update = "UPDATE alarms SET alarm_time=$1  WHERE alarm_name=$2;"
                    await self.db.execute(update, claim_reset, 'claim_reset')
                    update = "UPDATE w_players SET claim = 1 WHERE claim < 1"
                    await self.db.execute(update)
                await self.db.release(connection)

            if now > rolls_reset:
                rolls_reset = rolls_reset.add(hours=1)
                rolls_reset = formatter.pendulum_to_datetime(rolls_reset)

                connection = await self.db.acquire()
                async with connection.transaction():
                    update = "UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2"
                    await self.db.execute(update, rolls_reset, 'rolls_reset')
                    update = "UPDATE w_players SET rolls = 5 WHERE rolls != 5"
                    await self.db.execute(update)
                await self.db.release(connection)

            if now > decay_affinity:
                decay_affinity = decay_affinity.add(hours=4, minutes=48)
                decay_affinity = formatter.pendulum_to_datetime(decay_affinity)
                connection = await self.db.acquire()
                async with connection.transaction():
                    update = "UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2"
                    await self.db.execute(update, decay_affinity, 'decay_affinity')
                    update = "UPDATE w_card SET affinity = affinity-20 where owner is not NULL"
                    await self.db.execute(update)
                    await self.db.execute("UPDATE w_card SET owner = NULL, affinity = 100 WHERE affinity < 1")
                await self.db.release(connection)

            # Process role time assignment
            role_time = await self.db.fetch("select * from assign_roles")

            if role_time:
                for item in role_time:
                    server = self.get_guild(int(item['guild_id']))

                    if server:
                        member = server.get_member(item['user_id'])
                    else:
                        member = None

                    check_time = pendulum.instance(item['time'])

                    if (now > check_time):

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

                    else:
                        if member:
                            # Assign role if user doesn't have the role (and remove plankton if dunce)
                            role = discord.utils.get(member.roles, id=item['role_id'])
                            
                            if role is None:
                                role = discord.utils.get(server.roles, id=item['role_id'])
                                await member.add_roles(role)

            await asyncio.sleep(60)

    async def on_ready(self):
        print(f'{self.user.name} online!')
        print('----')
        await self.change_presence(activity=discord.Game('?help or Die!'))

    async def load_modules(self):
        modules = ['cogs.dbstuff', 'cogs.admin', 'cogs.fun', 'cogs.dc', 'cogs.waifugame']

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
            except Exception:
                pass


async def run():
    pg_credentials = {"user": CONFIG.USERNAME, "password": CONFIG.PASSWORD, "database": CONFIG.DATABASE,
                      "host": "127.0.0.1"}
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
    except Exception as e:
        print(e.__name__)
