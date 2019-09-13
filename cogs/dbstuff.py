from discord import Embed
from discord.ext import commands
from utils import formatter, SimplePaginator
import asyncio
import datetime
import pendulum


class DbCog(commands.Cog):
    """Database stuff"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list')
    async def list(self, ctx, *args):
        if ctx.message.channel.id in (167280538695106560, 360916876986941442, 378255860377452545, 458755509890056222):
            query_set={
                "query": '',
                "element": None,
                "rank": None,
                "role": None,
            }

            if args:
                for arg in args:
                    if arg.lower() in ("water", "fire", "forest", "dark", "light"):
                        query_set['element'] = arg.lower()
                    elif arg.lower() in ("attacker", "debuffer", "tank", "healer", "support"):
                        query_set['role'] = arg.lower()
                    elif arg.lower() in ("5", "4", "3"):
                        query_set['rank'] = ':star:' * int(arg)
                    else:
                        if query_set['query'] == '':
                            query_set['query'] = arg.lower()
                        else:
                            query_set['query'] = query_set['query'] + f' {arg}'.lower()

                if query_set['query'] != '':
                    query = "SELECT * FROM childs WHERE concat(child_call, alias1, alias2, name) similar to $1;"
                    invoke_records = await self.bot.db.fetch(query, f"%{query_set['query']}%")
                else:
                    query = f"SELECT * FROM childs;"
                    invoke_records = await self.bot.db.fetch(query)

                if query_set['element']:
                    invoke_records = [tup for tup in invoke_records if (tup['element'].lower() == query_set['element'])]

                if query_set['role']:
                    invoke_records = [tup for tup in invoke_records if (tup['role'].lower() == query_set['role'])]

                if query_set['rank']:
                    invoke_records = [tup for tup in invoke_records if (tup['rank'] == query_set['rank'])]

                if invoke_records:
                    # list results
                    result_list = [f"{'Name':<30}Search Term", ""]
                    for item in invoke_records:
                        terms = item['child_call']
                        if item['alias1']:
                            terms = f"{terms}, {item['alias1']}"
                        if item['alias2']:
                            terms = f"{terms}, {item['alias2']}"
                        result_list.append(f" {item['name']:<30}{terms}")
                    await SimplePaginator.SimplePaginator(entries=result_list, title='Results matching the criteria.',
                                                          length=20, embed=False).paginate(ctx)

                else:
                    await ctx.send('No results. Need help? <https://rodizipa.github.io/KirinusRewrite/#list>')
            else:
                # List all childs
                query = "SELECT child_call, alias1, alias2, name FROM childs"
                invoke_records = await self.bot.db.fetch(query)
                result_list = [f"{'Name':<25} Search Terms", ""]
                for item in invoke_records:
                    search = f"{item['child_call']}"
                    if item['alias1']:
                        search = search + f",{item['alias1']}"
                    if item['alias2']:
                        search = search + f",{item['alias2']}"

                    result_list.append(f" {item['name']:<26}{search}")
                await SimplePaginator.SimplePaginator(entries=result_list, title='Results matching the criteria.',
                                                      length=20, embed=False).paginate(ctx)

        else:
            await ctx.message.delete()
            await ctx.author.send("Don't use this cmd outside of bot channels.")

    @commands.command(name='child')
    async def child(self, ctx, *, child_call: str):
        """Search child info in database. Arguments: <child name>"""

        if ctx.message.channel.id in (167280538695106560, 360916876986941442, 378255860377452545, 458755509890056222):
            row = await self.bot.db.fetchrow("SELECT * FROM childs where similarity($1, child_call) > 0.8 ORDER BY $1 <-> child_call LIMIT 1", child_call.lower())
            # Checks if we got result or if we need to list:
            if row:
                em = await formatter.child_embed(row)
                await ctx.send(embed=em)
            else:
                row = await self.bot.db.fetchrow("SELECT * FROM childs WHERE similarity($1, alias1) > 0.8 ORDER BY $1 <-> alias1 LIMIT 1", child_call.lower())
                if row:
                    em = await formatter.child_embed(row)
                    await ctx.send(embed=em)
                else:
                    row = await self.bot.db.fetchrow(
                        "SELECT * FROM childs WHERE similarity($1, alias2) > 0.8 ORDER BY $1 <-> alias2 LIMIT 1", child_call.lower())
                    if row:
                        em = await formatter.child_embed(row)
                        await ctx.send(embed=em)
                    else:
                        rows = await self.bot.db.fetch("select * from childs where similarity($1, child_call) > 0.3 or similarity($1, alias1) > 0.3 or similarity($1, alias2) > 0.3 order by $1 <-> child_call LIMIT 5", child_call.lower())
                        description = "Child not found. Try using `?list` like `?list fire` or `?list mona`.\n"
                        if rows:
                            description = f"{description}\n**Possible matches:**\n"
                            for row in rows:
                                name = f"\n * **{row['name']}**: Use `{row['child_call']}`"
                                if row['alias1']:
                                    name = f"{name}, `{row['alias1']}`"
                                if row['alias2']:
                                    name=f"{name} or `{row['alias2']}`"
                                description = f"{description} {name}\n"

                        em = Embed(description=description)
                        await ctx.send(embed=em)
        else:
            await ctx.message.delete()
            await ctx.author.send("Don't use this cmd outside of bot channels.")

    @commands.command(name='quote', aliases=['tag'])
    async def quote(self, ctx, *args):
        """Search quote and return it on chat, if quote is img url, returns embed image.
        Alias: tag.
        Use: Adding tags: <add> <tagname> <content>. Check tag info: <info> <tag>. Tag search: <tag>
         """

        # List the Quotes in the paginator

        if not args or args[0] in ('list', 'help'):
            query = "SELECT invoke FROM quotes"
            invoke_records = await self.bot.db.fetch(query)
            invoke_list = []
            for item in invoke_records:
                invoke_list.append(item['invoke'])
            await SimplePaginator.SimplePaginator(entries=invoke_list, title='Kirinus Quote List', length=20, dm=True).paginate(ctx)
            await ctx.message.delete()

        # Add or update Tag
        elif args[0] == 'add':
            query = "SELECT * FROM quotes WHERE $1 = invoke;"
            row = await self.bot.db.fetchrow(query, args[1])
            connection = await self.bot.db.acquire()

            if row:
                async with connection.transaction():
                    update = "UPDATE quotes SET text = $1, created_at = $2, user_id = $3, created_by = $4 WHERE invoke = $5;"
                    await self.bot.db.execute(update, args[2], datetime.datetime.now(), ctx.author.id,
                                              ctx.author.display_name, args[1])
                await self.bot.db.release(connection)
                m = await ctx.send('Tag updated.')
                await asyncio.sleep(5)
                await m.delete()
            else:
                async with connection.transaction():
                    insert = "INSERT INTO quotes (invoke, text, created_by, created_at, user_id) VALUES ($1, $2, $3, $4, $5);"
                    await self.bot.db.execute(insert, args[1], args[2], ctx.author.name, datetime.datetime.now(),
                                              ctx.author.id)
                await self.bot.db.release(connection)
                m = await ctx.send('Tag created.')
                await asyncio.sleep(5)
                await m.delete()
            await ctx.message.delete()

        # Tag Info
        elif args[0] == 'info':
            query = "SELECT * FROM quotes WHERE $1 = invoke;"
            row = await self.bot.db.fetchrow(query, args[1])

            if row:
                em = await formatter.quote_info(ctx,row)
                m = await ctx.send(embed=em)
            else:
                m = await ctx.send("Try again when you know what you're searching for.")

            await ctx.message.delete()
            await asyncio.sleep(20)
            await m.delete()

        # Removes tag
        elif args[0] == 'remove':
            if ctx.author.id == 114010253938524167:
                query = "SELECT * FROM quotes WHERE $1 = invoke;"
                row = await self.bot.db.fetchrow(query, args[1])

                if row:
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        insert = "DELETE FROM quotes WHERE invoke = $1"
                        await self.bot.db.execute(insert, args[1])
                    await self.bot.db.release(connection)
                    m = await ctx.send("Tag Removed.")
                    await asyncio.sleep(5)
                    await m.delete()
                else:
                    m = await ctx.send("Come back when you know what You're doing.")
                    await asyncio.sleep(5)
                    await m.delete()
            else:
                m = await ctx.send("You have no permissions to do that D:<")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await m.delete()
        else:
                # Find item
                query = "SELECT * FROM quotes WHERE $1 = invoke;"
                row = await self.bot.db.fetchrow(query, args[0])
                if row:
                    em = await formatter.quote_embed(row)
                    em.set_footer(text="Invoked by: " + ctx.author.display_name)
                    await ctx.send(embed=em)
                    await ctx.message.delete()
                else:
                    m = await ctx.send("Quote not found.")
                    await asyncio.sleep(5)
                    await m.delete()

    @commands.command(name='reset')
    async def reset(self, ctx):
        """Countdown till next reset."""
        now = pendulum.now('Asia/Seoul')

        if now.hour > 3:
            quest_reset = pendulum.tomorrow('Asia/Seoul').add(hours=4)
        else:
            quest_reset = pendulum.today('Asia/Seoul').add(hours=4)

        reset_countdown = quest_reset.diff(now)
        em = Embed(description=f":alarm_clock: The next reset will happen in {reset_countdown.as_interval()}. :alarm_clock:")
        m = await ctx.send(embed=em)
        await asyncio.sleep(20)
        await ctx.message.delete()
        await m.delete()

    @commands.command(name='maint')
    async def maint(self, ctx, *args):
        """Countdown to maint. Args: <add> 'MM/DD HH/mm'"""

        # Add/Update maint
        if args:
            if args[0] == 'add':
                if ctx.author.id == 224522663626801152 or ctx.author.id == 114010253938524167:
                    query = "SELECT * FROM alarms WHERE $1 = alarm_name;"
                    row = await self.bot.db.fetchrow(query, 'maint')
                    connection = await self.bot.db.acquire()

                    # convert pen to datatime for saving in db

                    if len(args) == 3:
                        maint_time = pendulum.from_format(f'{args[1]} {args[2]}', 'MM/DD HH:mm', tz='Asia/Seoul')
                    else:
                        maint_time = pendulum.parse(args[1], tz='Asia/Seoul', strict=False)

                    maint_time = formatter.pendulum_to_datetime(maint_time)

                    if row:
                        async with connection.transaction():
                            update = "UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2;"
                            await self.bot.db.execute(update, maint_time, 'maint')
                        await self.bot.db.release(connection)
                        m = await ctx.send('Maint time updated.')
                        await asyncio.sleep(5)
                        await m.delete()
                    else:
                        async with connection.transaction():
                            insert = "INSERT INTO alarms (alarm_name, alarm_time) VALUES ($1, $2);"
                            await self.bot.db.execute(insert, 'maint', maint_time)
                        await self.bot.db.release(connection)
                        m = await ctx.send('Maint time created.')
                        await asyncio.sleep(5)
                        await m.delete()
                    await ctx.message.delete()
                else:
                    ctx.message.delete()
                    ctx.author.send("you have no permissions to do that.")

        # Normal Maint call
        else:
            query = "SELECT alarm_time FROM alarms WHERE alarm_name = $1;"
            row = await self.bot.db.fetchrow(query, 'maint')
            if row:
                maint_time = row['alarm_time']
                now = pendulum.now('Asia/Seoul')
                maint_time = pendulum.instance(maint_time, tz="Asia/Seoul")
                diff = maint_time.diff(now)

                if now > maint_time:
                    em = Embed(description=f":alarm_clock: Maint started {diff.as_interval()} ago. :alarm_clock:")
                else:
                    em = Embed(description=f':alarm_clock: Maint will start in {diff.as_interval()} from now. :alarm_clock:')

                m = await ctx.send(embed=em)
                await asyncio.sleep(20)
                await ctx.message.delete()
                await m.delete()

            else:
                m = await ctx.send("maint not yet created.")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await m.delete()


def setup(bot):
    bot.add_cog(DbCog(bot))
