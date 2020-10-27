import asyncio
import logging

import asyncpg
import discord
import pendulum
from discord.ext import commands

import CONFIG
from service.roleService import RoleService
from utils import formatter

logging.basicConfig(level=logging.WARN, filename='error.log')
intents = discord.Intents.default()
intents.members = True


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=CONFIG.PREFIX, description="Destiny Child KR bot.", intents=intents)
        self.__db = kwargs.pop("db")
        self.__roleService = RoleService(self)

    @property
    def db(self):
        return self.__db

    @property
    def roleservice(self):
        return self.__roleService

    async def on_command_completion(self, ctx):
        print(
            f'[{pendulum.now(tz="UTC").to_datetime_string()}] [Command] {ctx.message.content} by {ctx.author.name}')

    async def on_ready(self):
        print(f'{self.user.name} online!')
        print('----')
        await self.change_presence(activity=discord.Game('?help or Die!'))

    async def load_modules(self):
        modules = ['cogs.dbstuff', 'cogs.admin', 'cogs.fun', 'cogs.dc', 'cogs.karma']
        for extension in modules:
            self.load_extension(extension)

    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 723326060305055765:
            channel = await self.fetch_channel(channel_id=payload.channel_id)
            await self.user_role_self_management(payload, channel)

    async def user_role_self_management(self, payload, channel):
        role = await self.roleservice.find_reaction_role(payload.emoji.name)
        target_role = discord.utils.get(channel.guild.roles, id=role['role'])
        if target_role:
            user = payload.member
            await user.remove_roles(target_role) if discord.utils.get(user.roles, id=target_role.id) \
                else await user.add_roles(target_role)
        try:
            m = await channel.fetch_message(payload.message_id)
            await m.remove_reaction(payload.emoji, payload.member)
        except discord.HTTPException:
            pass

    async def on_message(self, message):
        if message.content.startswith('?'):
            await self.process_commands(message)
        else:
            try:
                role = await self.roleservice.fetch_member_role(message.author, "dunce")
                if role:
                    await formatter.kirinus_gacha(message)
            except discord.DiscordException as discord_exception:
                print("An discord error occurred. Logging.")
                logging.error(discord_exception.__name__, discord_exception)


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
    except Exception as ex:
        logging.error(ex.__name__)
