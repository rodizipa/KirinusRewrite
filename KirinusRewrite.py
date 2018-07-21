import discord
from discord.ext import commands
import asyncio
import asyncpg
import datetime
from time import gmtime, strftime
from utils import formatter
import CONFIG
import pendulum


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=CONFIG.PREFIX, description="Destiny Child KR bot.")
        self.db = kwargs.pop("db")
        self.wb_task = self.loop.create_task(self.world_boss_task())
        self.wb = self.WorldBoss()
        self.resets_task = self.loop.create_task(self.reset_task())

    class WorldBoss:
        def __init__(self, channel=None, status=False, first_run=False):
            self.channel = channel
            self.status = status
            self.first_run = first_run
            self.reset_time = 7200  # World Boss Reset

        def status_switch(self, value):
            if value:
                self.status = True
            else:
                self.status = False

        def first_run_switch(self, value):
            if value:
                self.first_run = True
            else:
                self.first_run = False

    async def reset_task(self):
        claim_reset = None
        rolls_reset = None
        while not self.is_closed():
            query = "select * from alarms where alarm_name = 'rolls_reset' or alarm_name = 'claim_reset'"
            rows = await self.db.fetch(query)
            for item in rows:
                if item['alarm_name'] == 'claim_reset':
                    claim_reset = pendulum.instance(item['alarm_time'])
                elif item['alarm_name'] == 'rolls_reset':
                    rolls_reset = pendulum.instance(item['alarm_time'])
            now = pendulum.now()

            if now > claim_reset:
                claim_reset = claim_reset.add(hours=3)
                claim_reset = datetime.datetime(claim_reset.year, claim_reset.month, claim_reset.day, claim_reset.hour,
                                                claim_reset.minute, claim_reset.second, claim_reset.microsecond,
                                                claim_reset.timezone)

                connection = await self.db.acquire()
                async with connection.transaction():
                    update = "UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2;"
                    await self.db.execute(update, claim_reset, 'claim_reset')
                    update = "UPDATE w_players SET claim = 1 WHERE claim < 1"
                    await self.db.execute(update)
                await self.db.release(connection)
            if now > rolls_reset:
                rolls_reset = rolls_reset.add(hours=1)
                rolls_reset = datetime.datetime(rolls_reset.year, rolls_reset.month, rolls_reset.day, rolls_reset.hour,
                                                rolls_reset.minute, rolls_reset.second, rolls_reset.microsecond,
                                                rolls_reset.timezone)
                connection = await self.db.acquire()
                async with connection.transaction():
                    update = "UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2;"
                    await self.db.execute(update, rolls_reset, 'rolls_reset')
                    update = "UPDATE w_players SET rolls = 5 WHERE rolls < 1"
                    await self.db.execute(update)
                await self.db.release(connection)
            await asyncio.sleep(1)

    async def world_boss_task(self):
        await self.wait_until_ready()
        self.wb.channel = self.get_channel(449061137523277834)  # Destiny Child Server
        # self.wb.channel = self.get_channel(167280538695106560)  #debug
        while not self.is_closed():
            while self.wb.status:
                if self.wb.first_run:
                    self.wb.first_run_switch(False)
                else:
                    m = await self.wb.channel.send("@here Ticket reset!")
                    await m.delete()
                    await self.wb.channel.send(embed=await formatter.wb_ticket_reset())
                await asyncio.sleep(self.wb.reset_time)
            await asyncio.sleep(1)

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
