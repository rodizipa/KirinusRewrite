import pendulum
from discord import Embed
from discord.ext import commands

from service.alarmsService import AlarmService
from service.childService import ChildService
from service.quoteService import QuoteService
from utils import formatter, SimplePaginator, helpers

TORONTO_TIME = "America/Toronto"
KR_TIME = 'Asia/Seoul'


class WrongChannel(commands.CheckFailure):
    pass


def auction_channel():
    async def predicate(ctx):
        if ctx.message.channel.id in (529546837661581312, 650512639012634626):
            return True
        raise WrongChannel('Wrong channel mate, only in waifu gacha.')

    return commands.check(predicate)


def bot_channel():
    async def predicate(ctx):
        if ctx.message.channel.id in (167280538695106560, 360916876986941442, 378255860377452545, 458755509890056222):
            return True
        raise WrongChannel('You cannot use this cmd outside of bot channels.')

    return commands.check(predicate)


def admin_check(ctx):
    return True if ctx.author.id == 224522663626801152 or ctx.author.id == 114010253938524167 else False


async def generate_search_list(ctx, invoke_records):
    result_list = [f"{'Name':<25}  Search Terms", " "]
    for item in invoke_records:
        search = f" {item['child_call']}"
        if item['alias1']:
            search = search + f", {item['alias1']}"
        if item['alias2']:
            search = search + f", {item['alias2']}"
        result_list.append(f"{item['name']:<26}{search}")
    await SimplePaginator.SimplePaginator(entries=result_list, title='Results matching the criteria.',
                                          length=20, embed=False).paginate(ctx)


async def quote_info_routine(ctx, quote):
    if quote:
        em = await formatter.quote_info(ctx, quote)
        await helpers.message_handler(em, ctx, 20, embed=True)
    else:
        await helpers.message_handler("Try again when you know what you're searching for.", ctx, 20)


class DbCog(commands.Cog):
    """Database stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.alarmService = AlarmService(self.bot)
        self.childService = ChildService(self.bot)
        self.quoteService = QuoteService(self.bot)

    async def add_alarm_routine(self, ctx, row, alarm, time, display_name):
        if row:
            await self.alarmService.update_alarm(alarm, time)
            await helpers.message_handler(f"{display_name} time updated.", ctx, 5)
        else:
            await self.alarmService.insert_alarm(alarm, time)
            await helpers.message_handler(f"{display_name} time created.", ctx, 5)

    async def quote_add_routine(self, ctx, args, quote):
        if quote:
            await self.quoteService.update_quote(ctx, args)
            await helpers.message_handler("Tag updated", ctx, 5)
        else:
            await self.quoteService.insert_quote(ctx, args)
            await helpers.message_handler("Tag created", ctx, 5)

    @commands.is_owner()
    async def quote_delete_routine(self, ctx, invoke, quote):
        if quote:
            await self.quoteService.delete_quote(invoke)
            await helpers.message_handler("Tag Removed.", ctx, 5)
        else:
            await helpers.message_handler("Come back when you know what You're doing.", ctx, 5)

    @bot_channel()
    @commands.command(name='list')
    async def list(self, ctx, *args):
        """List search terms by name, role, element, rank. `?list davi [optional fields: fire attacker 3]`"""
        if args:
            invoke_records = await self.childService.find_list_units(args)
            if invoke_records:
                await generate_search_list(ctx, invoke_records)
            else:
                await ctx.send('No results. Need help? <https://rodizipa.github.io/KirinusRewrite/#list>')
        else:
            invoke_records = await self.childService.list_all_keywords()
            await generate_search_list(ctx, invoke_records)

    @bot_channel()
    @commands.command(name='child')
    async def child(self, ctx, *, child_call: str):
        """Search child info in database. Arguments: <child name>"""
        row = await self.childService.find_one_similar(child_call)

        if row:
            em = await formatter.child_embed(row)
        else:
            rows = await self.childService.find_five_similar(child_call)
            description = "Child not found. Try using `?list` like `?list fire` or `?list mona`.\n"
            if rows:
                description = f"{description}\n**Possible matches:**\n"
                for row in rows:
                    unit = f"\n * **{row['name']}**: Use `{row['child_call']}`"
                    if row['alias1']:
                        unit = unit + f", `{row['alias1']}`"
                    if row['alias2']:
                        unit = unit + f" or `{row['alias2']}`"
                    description = f"{description} {unit}\n"
            em = Embed(description=description)
        await ctx.send(embed=em)

    @commands.command(name='quote', aliases=['tag'])
    async def quote(self, ctx, *args):
        """Search quote and return it on chat, if quote is img url, returns embed image.
        Alias: tag.
        Use: Adding tags: <add> <tagname> <content>. Check tag info: <info> <tag>. Tag search: <tag>
         """
        if not args or args[0] in ('list', 'help'):
            invoke_records = await self.quoteService.find_all()
            await SimplePaginator.SimplePaginator(entries=[item['invoke'] for item in invoke_records],
                                                  title='Kirinus Quote List', length=20, dm=True).paginate(ctx)
            await ctx.message.delete()
            return

        quote = await self.quoteService.find_one(args[1]) if args[0] in ('list', 'add', 'info', 'remove', 'help') else \
            await self.quoteService.find_one(args[0])
        if args[0] == 'add':
            await self.quote_add_routine(ctx, args, quote)
        elif args[0] == 'info':
            await quote_info_routine(ctx, quote)
        elif args[0] == 'remove':
            await self.quote_delete_routine(ctx, args[1], quote)
        else:
            if quote:
                em = await formatter.quote_embed(quote)
                em.set_footer(text="Invoked by: " + ctx.author.display_name)
                await helpers.message_handler(em, ctx, embed=True, delete=False)
            else:
                await helpers.message_handler("Quote not found.", ctx, 5)

    @commands.command(name='reset')
    async def reset(self, ctx):
        """Countdown till next reset."""
        now = pendulum.now(KR_TIME)
        quest_reset = pendulum.tomorrow(KR_TIME).add(hours=4) if now.hour > 3 else pendulum.today(KR_TIME).add(hours=4)

        reset_countdown = quest_reset.diff(now)
        em = Embed(
            description=f":alarm_clock: The next reset will happen in {reset_countdown.as_interval()}. :alarm_clock:")
        await helpers.message_handler(em, ctx, 20, embed=True)

    @commands.command(name='maint')
    async def maint(self, ctx, *args):
        """Countdown to maint. Args: <add> 'MM/DD HH/mm'"""

        row = await self.alarmService.get_alarm('maint')
        if args and args[0] == 'add':
            if admin_check(ctx):
                maint_time = pendulum.from_format(f'{args[1]} {args[2]}', 'MM/DD HH:mm', tz=KR_TIME) if len(args) == 3 \
                    else pendulum.parse(args[1], tz=KR_TIME, strict=False)
                maint_time = formatter.pendulum_to_datetime(maint_time)
                await self.add_alarm_routine(ctx, row, 'maint', maint_time, 'Maint')
            else:
                await helpers.message_denied("You have no permissions to do that", ctx, pm=True)
        else:
            if row:
                maint_time = row['alarm_time']
                maint_time = pendulum.instance(maint_time, tz=KR_TIME)
                now = pendulum.now(KR_TIME)
                diff = maint_time.diff(now)
                em = Embed(description=f":alarm_clock: Maint started {diff.as_interval()} ago. :alarm_clock:") if \
                    now > maint_time else Embed(
                    description=f':alarm_clock: Maint will start in {diff.as_interval()} from now. :alarm_clock:')
                await helpers.message_handler(em, ctx, 20, embed=True)
            else:
                await helpers.message_handler("Maint not yet created.", ctx, 5)

    @auction_channel()
    @commands.command(name='auction')
    async def auction(self, ctx, *args):
        """Countdown to auction. Args: <add> 'MM/DD HH/mm'"""

        row = await self.alarmService.get_alarm('auction')
        if args:
            if args[0] == 'add' and admin_check(ctx):
                auction_time = pendulum.from_format(f'{args[1]} {args[2]}', 'MM/DD HH:mm', tz=TORONTO_TIME) \
                    if len(args) == 3 else pendulum.parse(args[1], tz=TORONTO_TIME, strict=False)
                auction_time = formatter.pendulum_to_datetime(auction_time)
                await self.add_alarm_routine(ctx, row, 'auction', auction_time, 'Auction')
            else:
                await helpers.message_denied("you have no permissions to do that.", ctx, pm=True)
        else:
            if row:
                auction_time = row['alarm_time']
                now = pendulum.now(TORONTO_TIME)
                auction_time = pendulum.instance(auction_time, tz=TORONTO_TIME)
                diff = auction_time.diff(now)
                em = Embed(
                    description=f":alarm_clock: This ended exactly  {diff.as_interval()} ago mate. :alarm_clock:") if \
                    now > auction_time else Embed(
                    description=f':alarm_clock: Tic tac toc. {diff.as_interval()} remaining. :alarm_clock:')
                await helpers.message_handler(em, 20, embed=True)
            else:
                await helpers.message_handler("Auction not yet created.", 5)

    @auction.error
    async def auction_error(self, ctx, error):
        if isinstance(error, WrongChannel):
            await helpers.message_denied("Wrong channel mate, only in waifu gacha.", ctx, pm=True)

    @list.error
    @child.error
    async def bot_channel_error(self, ctx, error):
        if isinstance(error, WrongChannel):
            await helpers.message_denied("Don't use this cmd outside of bot channels.", ctx, pm=True)
        elif isinstance(error, commands.CommandInvokeError):
            await helpers.message_handler("Missing arguments", ctx, 5)
        else:
            print(error.__cause__)

    @quote.error
    async def quote_delete_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await helpers.message_handler("You have no permissions to do that D:<", ctx, 5)
        elif isinstance(error, commands.CommandInvokeError):
            await helpers.message_handler("Missing arguments", ctx, 5)
        else:
            print(error.__cause__)


def setup(bot):
    bot.add_cog(DbCog(bot))
