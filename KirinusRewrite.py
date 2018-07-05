import discord
from discord.ext import commands
import asyncio
import asyncpg
from time import gmtime, strftime
import CONFIG


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=CONFIG.PREFIX, description="Destiny Child KR bot.")

        self.db = kwargs.pop("db")

    async def on_ready(self):
        print(f'{self.user.name} online!')
        print('----')
        await self.change_presence(activity=discord.Game('?help or Die!'))

    async def load_modules(self):
        modules = ['cogs.dbstuff', 'cogs.admin', 'cogs.fun', 'cogs.dc']

        for extension in modules:
            self.load_extension(extension)


async def run():
    pg_credentials = {"user": CONFIG.USERNAME, "password": CONFIG.PASSWORD, "database": CONFIG.DATABASE,
                      "host": "127.0.0.1"}
    db = await asyncpg.create_pool(**pg_credentials)
    bot = Bot(db=db)
    try:
        await bot.load_modules()
        await bot.start(CONFIG.TOKEN)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()

if __name__ == '__main__':
    print("Starting bot...\n")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except Exception as e:
        print(e.__name__)
