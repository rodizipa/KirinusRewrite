from discord.ext import commands
import discord
import asyncio
import random
import pendulum
from utils import SimplePaginator, formatter


# Check if message is sent in bot channel
def is_bot_channel():
    async def predicate(ctx):
        if ctx.message.channel.id == 485905859793125376 or ctx.message.channel.id == 167280538695106560:
            return True
        else:
            await ctx.message.delete()
            await ctx.author.send("Do not use this command outside of waifu gacha channel.")
            return False
    return commands.check(predicate)


# Check if user has a claim point and informs user
async def has_claim(ctx, target):
    query = 'select * from w_players where owner_id = $1'
    user = await ctx.bot.db.fetchrow(query, target.id)

    if user:
        if int(user['claim']) > 0:
            return True
        else:
            query = "select * from alarms where alarm_name = 'claim_reset'"
            row = await ctx.bot.db.fetchrow(query)
            claim_time = pendulum.instance(row['alarm_time'])
            await ctx.send(f"{target.mention}. You can't claim now. You will receive a claim in  {claim_time.diff().as_interval()}")
            return False
    else:
        print(f"{target.display_name} tried to claim but doesn't exist in the database.")
        return False


async def consume_claim(ctx, target):
    query = 'select * from w_players where owner_id = $1'
    user = await ctx.bot.db.fetchrow(query, target.id)
    connection = await ctx.bot.db.acquire()
    update= 'UPDATE w_players SET claim = $1 WHERE owner_id = $2'
    async with connection.transaction():
        await ctx.bot.db.execute(update, int(user['claim'])-1, target.id)
    await ctx.bot.db.release(connection)


async def consume_roll(ctx):
    query = 'select * from w_players where owner_id = $1'
    user = await ctx.bot.db.fetchrow(query, ctx.author.id)
    connection = await ctx.bot.db.acquire()
    update = 'UPDATE w_players SET rolls = $1 WHERE owner_id = $2'
    async with connection.transaction():
        await ctx.bot.db.execute(update, int(user['rolls']) - 1, ctx.author.id)
    await ctx.bot.db.release(connection)


# Check if user has roll
def user_has_roll():
    async def predicate(ctx):
        query = 'select * from w_players where owner_id = $1'
        user = await ctx.bot.db.fetchrow(query, ctx.author.id)

        if user['rolls'] > 0:
            return True
        else:
            query = "select * from alarms where alarm_name = 'rolls_reset'"
            row = await ctx.bot.db.fetchrow(query)
            reset_time = pendulum.instance(row['alarm_time'])
            if reset_time > pendulum.now():
                await ctx.send(
                f"{ctx.author.mention}. You used all your rolls, roll reset will happen in: {reset_time.diff().as_interval()}")
            else:
                await ctx.send(f'Processing roll reset, come back soon.')
            return False

    return commands.check(predicate)


def user_exist():
    async def predicate(ctx):
        query = 'select * from w_players where owner_id = $1'
        user = await ctx.bot.db.fetchrow(query, ctx.author.id)

        if user:
            return True
        else:
            connection = await ctx.bot.db.acquire()
            insert = 'insert into w_players(owner_id, claim, rolls) VALUES($1,$2,$3)'
            async with connection.transaction():
                await ctx.bot.db.execute(insert, ctx.author.id, 1, 5)
            await ctx.bot.db.release(connection)
            return True
    return commands.check(predicate)


class WaifuInstance:
    def __init__(self, bot):
        self.bot = bot
        self.base = None
        self.embed = None
        self.timeout = 45
        self.message = None
        self.controls = {'💌': 'marry', '✅': 'confirm', '❎': 'refuse'}
        self.confirmation = None

    async def confirmation_control(self, ctx, target):
        bot = ctx.bot
        await self.base.add_reaction('✅')
        await self.base.add_reaction('❎')

        def check(r, u):
            if str(r) not in self.controls.keys():
                return False
            elif u.id == bot.user.id or r.message.id != self.base.id:
                return False
            elif u.id != target.id:
                return False
            return True

        while True:
            try:
                react, user = await bot.wait_for('reaction_add', check=check, timeout=self.timeout)
            except asyncio.TimeoutError:
                await self.base.delete()
                await ctx.send("I have better things to do instead of waiting your answer.")
                return ctx.message.delete()

            control = self.controls.get(str(react))

            try:
                await self.base.remove_reaction(react, user)
            except discord.HTTPException:
                pass

            if control == 'confirm':
                await self.base.delete()
                return True

            if control == 'refuse':
                await self.base.delete()
                return False

    async def marry_control(self, ctx, waifu):
        bot = ctx.bot
        await self.base.add_reaction('💌')

        def check(r, u):
            if str(r) not in self.controls.keys():
                return False
            elif u.id == bot.user.id or r.message.id != self.base.id:
                return False
            return True

        while True:
            try:
                react, user = await bot.wait_for('reaction_add', check=check, timeout=self.timeout)
            except asyncio.TimeoutError:
                await self.base.clear_reactions()
                return False

            control = self.controls.get(str(react))

            try:
                await self.base.remove_reaction(react, user)
            except discord.HTTPException:
                pass

            if control == 'marry':
                confirm_claim = await has_claim(ctx, user)

                if confirm_claim is True:
                    connection = await self.bot.db.acquire()
                    insert = 'UPDATE w_card SET owner = $1  WHERE child_id = $2;'
                    async with connection.transaction():
                        await self.bot.db.execute(insert, user.id, waifu['child_id'])
                    await self.bot.db.release(connection)
                    self.embed.set_footer(text=f'Belongs to {user.display_name}', icon_url=user.avatar_url)
                    await self.base.edit(embed=self.embed)
                    await self.base.remove_reaction(react, bot.user)
                    await consume_claim(ctx, user)
                    await ctx.send(f"💟 {waifu['name']} now belongs to {user.display_name} 💟")
                    return True


class WaifuCog(commands.Cog):
    """Commands related to Waifu Gacha Minigame"""
    def __init__(self, bot):
        self.bot = bot

    #roll units
    @commands.command(name='waifu', aliases=['w'])
    @is_bot_channel()
    @commands.guild_only()
    @user_exist()
    @user_has_roll()
    async def waifu_roll(self, ctx):
        """Get random Candidate costing a roll point. Aliases: ?w. Roll point recharged each 1h."""
        await consume_roll(ctx)
        query = "select * from waifu_view order by random() limit 1;"
        waifu_card = await self.bot.db.fetchrow(query)
        # Jackpot
        if random.randrange(1, 100) < 4:

            value = random.randint(1, 5)
            updatecoins = "UPDATE w_players SET coins = coins + $1 WHERE owner_id = $2;"
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                await self.bot.db.execute(updatecoins, value, ctx.author.id)
            await self.bot.db.release(connection)
            await ctx.send(f"<:kiri:431294173614964736> Jackpot! {ctx.author.mention} got {value} kiricoins <:kiri:431294173614964736>")

        em = discord.Embed(title=waifu_card['name'])
        if waifu_card['picture']:
            em.set_image(url=waifu_card['picture'])
        # Already Owned Card
        if waifu_card['owner']:
            foot_owner = ctx.guild.get_member(waifu_card['owner'])
            if not foot_owner:
                foot_owner = self.bot.get_user(waifu_card['owner'])
            em.set_footer(text=f'Belongs to {foot_owner.display_name}', icon_url=foot_owner.avatar_url)
            await ctx.send(embed=em)
        else:
            waifuclass = WaifuInstance(self.bot)
            waifuclass.embed = em
            waifuclass.base = await ctx.send(embed=em)
            waifuclass.instance = await ctx.bot.loop.create_task(waifuclass.marry_control(ctx, waifu_card))

        

    # list owned units by user
    @commands.guild_only()
    @is_bot_channel()
    @commands.command(name='waifulist', aliases=['wl'])
    async def waifulist(self, ctx):
        """Lists all units claimed by author or mentioned user. aliases: wl"""
        if ctx.message.mentions:
            target = ctx.message.mentions[0]
        else:
            target = ctx.author
        query = "select * from waifu_view where owner = $1"
        records = await self.bot.db.fetch(query, target.id)
        m = None

        if records:
            records_list = [""]
            for item in records:
                records_list.append(f"{item['name']} {item['affinity']}❤")

            #check if favorite exists
            query = "select favorite_child from w_players where owner_id = $1"
            row = await self.bot.db.fetchrow(query, target.id)

            if row:
                await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10,author=target, favorite=row['favorite_child']).paginate(ctx)
            else:
                await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10, author=target).paginate(ctx)
        else:
            m = await ctx.send(f"{target.display_name}'s harem is empty.")
        await asyncio.sleep(10)
        await ctx.message.delete()
        if m:
            await m.delete()

    # check claim
    @commands.guild_only()
    @is_bot_channel()
    @user_exist()
    @commands.command(name='waifuclaim', aliases=['wc'])
    async def waifuclaim(self, ctx):
        """Check if user has claim, and when reset happens. alias:wc"""
        query = 'select * from w_players where owner_id = $1'
        user = await ctx.bot.db.fetchrow(query, ctx.author.id)
        query2 = "select * from alarms where alarm_name = 'claim_reset'"
        row = await ctx.bot.db.fetchrow(query2)
        claim_time = pendulum.instance(row['alarm_time'])

        if int(user['claim']) > 0:
            await ctx.send(f"{ctx.author.mention}. You can claim now (You own {user['claim']}). You will receive a claim in {claim_time.diff().as_interval()}")
        else:
            await ctx.send(
                f"{ctx.author.mention}. You can't claim now. You will receive a claim in {claim_time.diff().as_interval()}")

    # set favorite
    @commands.guild_only()
    @is_bot_channel()
    @commands.command(name='favoritewaifu', aliases=['fw'])
    async def favoritewaifu(self, ctx, *args):
        """Set child as your waifu list avatar."""
        fav_unit = " ".join(args)
        if not args:
            m = await ctx.send("Include child name in the arguments. Example: `?fw kirinus`")
            await asyncio.sleep(10)
            await m.delete()
            await ctx.message.delete()
            return False
        query = "SELECT * FROM childs WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
        waifu_card = await self.bot.db.fetchrow(query, fav_unit)
        if waifu_card:
            connection = await self.bot.db.acquire()
            update = "UPDATE w_players SET favorite_child = $1  WHERE owner_id = $2"
            async with connection.transaction():
                await self.bot.db.execute(update, waifu_card['thumbnail'], ctx.author.id)
            await self.bot.db.release(connection)
            await ctx.send("Favorite child updated.")
        else:
            m = await ctx.send("Child not found.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()

    # search named unit
    @commands.guild_only()
    @is_bot_channel()
    @commands.command(name='waifuinfo', aliases=['wi'])
    async def waifuinfo(self, ctx, *, name: str):
        """Search the unit and display the info. Alias: wi"""
        query = "SELECT * FROM waifu_view WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
        waifu_card = await self.bot.db.fetchrow(query, name)
        em = discord.Embed(title=waifu_card['name'], description=f"❤ {waifu_card['affinity']}")
        if waifu_card['picture']:
            em.set_image(url=waifu_card['picture'])
        # Already Owned Card
        if waifu_card['owner']:
            foot_owner = ctx.guild.get_member(waifu_card['owner'])

            if foot_owner:
                em.set_footer(text=f'Belongs to {foot_owner.display_name}', icon_url=foot_owner.avatar_url)
            else:
                em.set_footer(text=f'Owner left the server.', icon_url='https://cdn.discordapp.com/emojis/348280846987558912.png?v=1')
        await ctx.send(embed=em)

    # release waifu
    @commands.guild_only()
    @is_bot_channel()
    @commands.command(name='waifurelease', aliases=['wr'])
    async def waifurelease(self, ctx, *, name: str):
        """Releases unit that you own. alias: wr"""
        query = "SELECT * FROM waifu_view WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
        row = await self.bot.db.fetchrow(query, name)

        if not row:
            await ctx.send("child doesn't exist")
            return False

        if row['owner'] == ctx.author.id:
            waifuclass = WaifuInstance(self.bot)
            em = discord.Embed(title="Confirmation", color=discord.colour.Colour.dark_red(),
                                             description="Do you really want to release this child?")
            waifuclass.base = await ctx.send(embed=em)
            fut = await ctx.bot.loop.create_task(waifuclass.confirmation_control(ctx, ctx.author))
            if fut is True:
                connection = await self.bot.db.acquire()
                insert = 'UPDATE w_card SET owner = null, affinity = 100  WHERE child_id = $2 and owner = $1;'
                async with connection.transaction():
                    await self.bot.db.execute(insert, ctx.author.id, row['child_id'])
                await self.bot.db.release(connection)
                await ctx.send(f"💔 {ctx.author.display_name} divorced with {row['name']}.💔")
            elif fut is False:
                m = await ctx.send("Ok then.")
                await asyncio.sleep(5)
                await m.delete()
                await ctx.message.delete()
        else:
            m = await ctx.send("You do not own this child.")
            await asyncio.sleep(5)
            await m.delete()
            await ctx.message.delete()

    #trade system
    @commands.guild_only()
    @is_bot_channel()
    @commands.command(name='waifutrade', aliases=['wt', 'we', 'waifuexchange'])
    async def waifutrade(self, ctx, *args):
        """Trade your waifu with another player."""

        if not args or len(ctx.message.mentions) == 0:
            await ctx.send(f"{ctx.author.mention}, mention a user when starting the trade.")
            return False

        # author list
        query = "select name, affinity from waifu_view where owner = $1"
        records = await self.bot.db.fetch(query, ctx.author.id)
        if records:
            records_list = [""]
            for item in records:
                records_list.append(f"{item['name']} {item['affinity']}❤")
            # check if favorite exists
            query = "select favorite_child from w_players where owner_id = $1"
            fav = await self.bot.db.fetchrow(query, ctx.author.id)
            if fav:
                await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10,
                                                     author=ctx.author, favorite=fav['favorite_child']).paginate(ctx)
            else:
                await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10,
                                                      author=ctx.author).paginate(ctx)
        else:
            await ctx.send("You or the user indicated don't have anyone.")
            return False

        # Receive author answer
        await ctx.send(f"{ctx.author.mention}, type the name of the child you want to trade.")

        def check(m):
            return m.author == ctx.author

        try:
            answer = await ctx.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You're wasting my computational time.")
            return False

        if answer:
            # Check if owns:
            query = "SELECT * FROM waifu_view WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
            row = await self.bot.db.fetchrow(query, answer.content)
            if not row:
                await ctx.send("Child doesn't exist or invalid name.")
            if row['owner'] != ctx.author.id:
                await ctx.send("You're not the owner of this unit.")
                return False
            # In case author was owner of the previous child.
            query = "select name, affinity from waifu_view where owner = $1"
            records = await self.bot.db.fetch(query, ctx.message.mentions[0].id)
            if records:
                records_list = [""]
                for item in records:
                    records_list.append(f"{item['name']} {item['affinity']} ❤")
                query = "select favorite_child from w_players where owner_id = $1"
                fav = await self.bot.db.fetchrow(query, ctx.message.mentions[0].id)
                if fav:
                    await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10,
                                                          author=ctx.message.mentions[0], favorite=fav['favorite_child']).paginate(ctx)
                else:
                    await SimplePaginator.SimplePaginator(entries=records_list, title='', length=10,
                                                          author=ctx.message.mentions[0]).paginate(ctx)
            else:
                await ctx.send("You or the user indicated don't have anyone.")
                return False

            # Receive Mentioned user answer:
            await ctx.send(f"{ctx.message.mentions[0].mention}, type the name of the child you want to trade.")

            def check(m):
                return m.author == ctx.message.mentions[0]
            try:
                answer2 = await ctx.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("You're wasting my computational time.")
                return False

            # Check if mentioned user is owner:
            query2 = "SELECT * FROM waifu_view WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
            row2 = await self.bot.db.fetchrow(query2, answer2.content)
            if not row2:
                await ctx.send("Child doesn't exist or invalid name.")
            if row2['owner'] != ctx.message.mentions[0].id:
                await ctx.send("You're not the owner of this unit.")
                return False

            # confirm trade:
            answer4 = None

            waifuclass = WaifuInstance(self.bot)
            waifuclass.base = await ctx.send(f"{ctx.message.mentions[0].mention}, you're receiving {row['name']} do you confirm?")
            answer3 = await ctx.bot.loop.create_task(waifuclass.confirmation_control(ctx, ctx.message.mentions[0]))
            del waifuclass

            if answer3 is True:
                waifuclass = WaifuInstance(self.bot)
                waifuclass.base = await ctx.send(f"{ctx.author.mention}, you're receiving {row2['name']}, do you confirm?")
                answer4 = await ctx.bot.loop.create_task(waifuclass.confirmation_control(ctx, ctx.author))

            if answer3 and answer4:
                connection = await self.bot.db.acquire()
                insert = 'UPDATE w_card SET owner = $3  WHERE child_id = $2 and owner = $1;'
                insert2 = 'UPDATE w_card SET owner = $3  WHERE child_id = $2 and owner = $1;'
                async with connection.transaction():
                    await self.bot.db.execute(insert, ctx.author.id, row['child_id'], ctx.message.mentions[0].id)
                    await self.bot.db.execute(insert2, ctx.message.mentions[0].id, row2['child_id'], ctx.author.id)
                await self.bot.db.release(connection)
                await ctx.send("🤝Trade Completed.🤝")
            else:
                await ctx.send("🛑Trade canceled.🛑")

    # statistics
    @is_bot_channel()
    @commands.command(name='waifustatistics', aliases=['ws'])
    async def waifustatistics(self, ctx):
        total_childs = await self.bot.db.fetchrow("select count(*) from w_card")
        childs_claimed = await self.bot.db.fetchrow("select count(*) from w_card where owner is not null")
        five_stars_claimed = await self.bot.db.fetchrow("SELECT count(*) from waifu_view where rank = ':star::star::star::star::star:' and owner is not null")
        total_five_stars = await self.bot.db.fetchrow("SELECT count(*) from waifu_view where rank = ':star::star::star::star::star:'")
        em = discord.Embed(title="Waifu Statistics", description=f"{childs_claimed['count']}/{total_childs['count']} units claimed.\n 5 stars: "
                                                                 f"{five_stars_claimed['count']}/{total_five_stars['count']}")
        await ctx.send(embed=em)

    # Change card icon
    @commands.is_owner()
    @is_bot_channel()
    @commands.command(name='waifupic', aliases=['wp'])
    async def waifupicture(self, ctx, *args):
        """Change waifu card picture. Admin only."""
        if not args:
            m = await ctx.send("Invalid or missing argument. `?wp <name> <image_url>`")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()
            return False

        query = "SELECT child_id from childs where LOWER($1) in (LOWER(name), child_call, alias1, alias2);"
        child_id = await self.bot.db.fetchrow(query, args[0])

        if child_id:
            connection = await self.bot.db.acquire()
            update = "UPDATE w_card SET picture = $1 where child_id = $2;"
            async with connection.transaction():
                await self.bot.db.execute(update, args[1], child_id['child_id'])
            await self.bot.db.release(connection)
            m = await ctx.send("Picture updated.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()
        else:
            m = await ctx.send("Unit not found.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()

    @commands.command(name="dailies", aliases=["daily"])
    @is_bot_channel()
    @user_exist()
    async def dailies(self, ctx):
        query = "select daily_claim from w_players where owner_id = $1"
        row = await ctx.bot.db.fetchrow(query, ctx.author.id)
        claim_time = None
        if row['daily_claim']:
            claim_time = pendulum.instance(row['daily_claim'])
            next_reset = claim_time.add(hours=20)
        else:
            next_reset = None

        now = pendulum.now()
        now_dt = formatter.pendulum_to_datetime(now)

        if claim_time is None:
            update = "UPDATE w_players SET daily_claim = $1  WHERE owner_id = $2;"
            updatecoins = "UPDATE w_players SET coins = $1 WHERE owner_id = $2;"
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                await self.bot.db.execute(update, now_dt, ctx.author.id)
                await self.bot.db.execute(updatecoins, 20, ctx.author.id)
            await self.bot.db.release(connection)
            await ctx.send(embed=discord.Embed(description=":atm: You received 20 <:kirinuscoin:471161189574115338>. Don't spend it all on candy."))

        elif now > next_reset:
            update = "update w_players set daily_claim = $1 where owner_id = $2"
            updatecoins = "update w_players set coins = coins + $1 where owner_id = $2"
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                await self.bot.db.execute(update, now_dt, ctx.author.id)
                await self.bot.db.execute(updatecoins, 10, ctx.author.id)
            await self.bot.db.release(connection)
            await ctx.send(embed=discord.Embed(description=":atm: You received 10 <:kirinuscoin:471161189574115338>. Don't spend it all on candy."))
        elif now < next_reset:
            m = await ctx.send(embed=discord.Embed(description=f"You already claimed your coins in the last 20 hours. Time left: {now.diff(next_reset).as_interval()}"))
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()
        else:
            print(f"User {ctx.author.display-name} tried to claim dailies and an error ocurred.")

    @is_bot_channel()
    @user_exist()
    @commands.command(name='balance', aliases=['inventory', 'bag', 'b'])
    async def balance(self, ctx):
        user = await ctx.bot.db.fetchrow("select coins, skewers from w_players where owner_id = $1", ctx.author.id)

        if user['coins'] is None:
            m = await ctx.send(embed=discord.Embed(description="You have no bank account yet. Try ?dailies to get one now."))
        else:
            m = await ctx.send(embed=discord.Embed(description=f"Current balance: {user['coins']} kiricoins >\n <:skewers:471718924237406209> Skewers owned: {user['skewers']}"))

        await asyncio.sleep(10)
        await ctx.message.delete()
        await m.delete()

    @is_bot_channel()
    @user_exist()
    @commands.command(name='shop', aliases=['s'])
    async def kirishop(self, ctx, *args):
        repeat = 1

        if args:
            answer = args[0]
            if len(args) > 1:
                repeat = int(args[1])
        else:

            await ctx.send(embed=discord.Embed(title="Kirinus' Tent", description="Ey there,young'un. Delicious skewers for only 1 buck. (Type the Number)\n\n 1 - <:skewers:471718924237406209> Buy Skewer (1 kiricoin)\n"
                                                                            "2 - <:skewers:471718924237406209> Buy 10x Skewers (10 kiricoins)\n 3 - U Know what, give me a extra claim (10 kiricoins)\n 4 - Nevermind."))

            def check(m):
                return m.author == ctx.author

            try:
                answer = await ctx.bot.wait_for('message', check=check, timeout=60)
                answer = answer.content
            except asyncio.TimeoutError:
                await ctx.send("I will not give you anything if u just stare u know. NEXT!")
                return False

        while repeat > 0:
            user = await ctx.bot.db.fetchrow("select coins from w_players where owner_id = $1", ctx.author.id)
            coins = user['coins']

            if coins is None:
                await ctx.send("You never received a kiri coin, type `?dailies` to get it now!")
                return True

            if answer == '1':
                if coins < 1:
                    await ctx.send("Bah, come back when you have money to pay young one.")
                    break
                else:
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        await self.bot.db.execute("UPDATE w_players set coins = $1, skewers = skewers + 1 where owner_id = $2", coins-1, ctx.author.id)
                        await ctx.send(f"You bought 1 skewer, now you have {coins-1} kiricoins")
                    await self.bot.db.release(connection)
            elif answer == '2':
                if coins < 10:
                    await ctx.send("Bah, come back when you have money to pay pal.")
                    break
                else:
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        await self.bot.db.execute("UPDATE w_players set coins = $1, skewers = skewers + 10 where owner_id = $2",
                                                  coins - 10, ctx.author.id)
                        await ctx.send(f"You bought 10 skewers, now you have {coins-10} kiricoins")
                    await self.bot.db.release(connection)
            elif answer == '3':
                if coins < 10:
                    await ctx.send("You don't have all this money kiddo.")
                    break
                else:
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        await self.bot.db.execute("UPDATE w_players set coins = $1, claim = claim + 1 where owner_id = $2",
                                                  coins - 10, ctx.author.id)
                        await ctx.send(f"You bought a extra claim, now you have {coins-10} kiricoins")
                    await self.bot.db.release(connection)
            elif answer == '4':
                await ctx.send("You sure? Ok, come back soon!")
            repeat = repeat - 1


    @is_bot_channel()
    @commands.command("feed")
    async def feed(self, ctx, *args):

        if len(args) == 0:
            await ctx.send(f"{ctx.author.mention}. You need to indicate who you're feeding. `?feed kirinus`.")
            return True

        child_name = " ".join(args)

        unit = await ctx.bot.db.fetchrow(
            "SELECT * FROM waifu_view WHERE LOWER($1) in (LOWER(name), child_call, alias1, alias2);", child_name)

        if unit:
            if unit['owner'] == ctx.author.id:
                await ctx.send(f"{ctx.author.mention} Insert the amounts of skewers you want to feed: ")

                def check(m):
                    return m.author == ctx.author

                try:
                    answer = await ctx.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await ctx.send(f"{ctx.author.mention}. I have other units to feed u know.")
                    return False

                if answer.content.isdigit():
                    user = await ctx.bot.db.fetchrow("select coins, skewers from w_players where owner_id = $1",
                                                     ctx.author.id)

                    if int(answer.content) > user['skewers']:
                        await ctx.send(f"{ctx.author.mention}. You do not own enough skewers for that.")
                        return True
                    else:
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            await self.bot.db.execute(
                                "UPDATE w_players set skewers = skewers - $1 where owner_id = $2",
                                int(answer.content), ctx.author.id)
                            await self.bot.db.execute("UPDATE w_card set affinity = affinity + $1 where child_id = $2", int(answer.content) * 20, unit['child_id'])
                            await ctx.send(f"❤ {unit['name']}'s affinity increased in {int(answer.content) * 20} ❤")
                        await self.bot.db.release(connection)

                else:
                    await ctx.send("Insert a digit next time.")
                    return True
            else:
                await ctx.send("You do not own this unit.")
                return True
        else:
            await ctx.send("Unit not found.")
            return True

    @commands.is_owner()
    @commands.command(name="resetclaims")
    async def reset_claim(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            await self.bot.db.execute("UPDATE w_players set claim = 1, rolls = 5, coins = coins + 10")
            await ctx.send(f"Reset completed")
        await self.bot.db.release(connection)


def setup(bot):
    bot.add_cog(WaifuCog(bot))
