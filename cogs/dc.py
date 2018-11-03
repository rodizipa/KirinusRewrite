from discord.ext import commands
from utils.formatter import element_color
from discord import Embed, utils
import datetime
import asyncio
import random


class DcCogs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='raid')
    async def raid(self, ctx, *args):
        """Call raids announcement. args: [optional: Owner (mention)], [optional: level : number], [optional: name]"""
        if ctx.message.channel.id == 167280538695106560 or ctx.message.channel.id == 477146466607955971 or ctx.message.channel.id == 504862373459525643:

            m = await ctx.send("@here")

            # Set raid owner
            if ctx.message.mentions:
                owner = ctx.message.mentions[0].display_name
            else:
                owner = ctx.author.display_name

            # default raid alert
            em = Embed(colour=await element_color('Dark'), title="Raid Alert!", description=f"@here, {owner} found a raid!", timestamp=datetime.datetime.now())
            em.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/504999706922057729/ragnadaviraid.png")

            level = None
            raid_call = None
            # If argument exists
            if args:
                for item in args:
                    if item.isdigit():
                        level = item
                    elif not item.startswith('<'):
                        raid_call = item.lower()

            # If raid tag exists
            if raid_call:
                if raid_call == 'aria':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found an Aria!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438159951986708/Aria.png")

                elif raid_call == 'davi':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a Davi!'
                    em.set_image(url='https://cdn.discordapp.com/attachments/448341812055244817/504999706922057729/ragnadaviraid.png')

                elif raid_call == 'navi':
                    em.colour = await element_color('Fire')
                    em.description = f'@here, {owner} found a Navi!'
                    em.set_image(url='https://cdn.discordapp.com/attachments/448341812055244817/504999710608850944/naviragna.png')

                elif raid_call == 'cocoon':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a Cocoon!'
                    em.set_image(url='https://cdn.discordapp.com/attachments/448341812055244817/504999704401281034/fusionmachineragna.png')

                elif raid_call == 'doll':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a Doll!'
                    em.set_image(url='https://cdn.discordapp.com/attachments/448341812055244817/504999696884957194/dollragna.png')

                elif raid_call in ('cleo', 'cleopatra'):
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418781949465722880/dorrow_cleo.png")

                elif raid_call in 'demeter':
                    em.colour = await element_color('Fire')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/448342259406995486/demeter.png")

                elif raid_call in ('slime', 'pancakes'):
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418594680528437278/something_smaller.png")

                elif raid_call in 'morgan':
                    em.colour = await element_color('Fire')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438370388475914/morgan.png")

                elif raid_call in 'rita':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438469042831370/rita.png")

                elif raid_call in 'krampus':
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438405054529537/krampus.png")

                elif raid_call in ('abaddon', 'abadon', 'abbadon'):
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found an {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/450101110850715648/abaddon.png")

                elif raid_call in 'frey':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438459756642305/Frey.png")

                elif raid_call in 'anemone':
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found an {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438523338096640/anemone.png")

                elif raid_call in ('iseult', 'isolde'):
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found an {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438528870383616/isolde.png")

                elif raid_call in ('verd', 'verdel', 'verdelet'):
                    em.colour = await element_color('Fire')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438373009915924/verd.png")

                elif raid_call in 'mars':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438164578304015/Mars.png")

                elif raid_call in 'neptune':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438171058372628/Neptune.png")

                elif raid_call in 'saturn':
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438173985996810/Saturn.png")

                elif raid_call in 'bari':
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438224753852416/bari.png")

                elif raid_call in 'santa':
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438412893552640/santa.png")

                elif raid_call in ('willow', 'bachelor'):
                    em.colour = await element_color('Water')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438249588326400/willow.png")

                elif raid_call in 'tristan':
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438531726573569/tristan.png")

                elif raid_call in 'apep':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found an {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438292902903851/apep.png")

                elif raid_call in 'bast':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438297613369354/bastet.png")

                elif raid_call in 'horus':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438314176413696/horus.png")

                elif raid_call in ('hildr', 'hilde'):
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/474773560922079233/hildrraid.png")

                elif raid_call in 'neman':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438463892226068/Neman.png")

                elif raid_call == 'nicole':
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438410498736148/nicole.png")

                elif raid_call == 'pomona':
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/474773578773168129/pomonaraid.png")

                elif raid_call == 'iphis':
                    em.colour = await element_color('Light')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/448341812055244817/474773568660439060/iphisraid.png")

                else:
                    em.description = f'@here, {owner} found a/an {raid_call}'

            if level:
                em_edit = em.description
                em.description = em_edit + f"\nAlso, appears to be lvl **{level}**.\n"

            await m.delete()
            await ctx.send(embed=em)
            await ctx.message.delete()

            if random.randrange(1, 100) < 3:
                value = random.randint(1, 5)
                updatecoins = "UPDATE w_players SET coins = coins + $1 WHERE owner_id = $2;"
                connection = await self.bot.db.acquire()
                async with connection.transaction():
                    await self.bot.db.execute(updatecoins, value, ctx.author.id)
                await self.bot.db.release(connection)
                await ctx.send(
                    f"<:kiri:431294173614964736> Jackpot! {ctx.author.mention} got {value} kiricoins <:kiri:431294173614964736>")
        else:
            await ctx.message.delete()
            await ctx.author.send("You can't do raid call outside of raid channel.")

    @commands.command(name="wb")
    async def wb_cmd(self, ctx, *args):
        if args[0] == 'join':
            try:
                role = utils.get(ctx.author.roles, id=295083791884615680)
                if role:
                    wb_role = utils.get(ctx.guild.roles, id=494856310844686337)
                    await ctx.author.add_roles(wb_role)
                    m = await ctx.send("You have joined the WB squad.")
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await m.delete()
            except Exception:
                await asyncio.sleep(1)
                await ctx.message.delete()

        elif args[0] == 'leave':
            wb_role = utils.get(ctx.guild.roles, id=494856310844686337)
            await ctx.author.remove_roles(wb_role)
            m = await ctx.send("You left the WB squad.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await m.delete()


def setup(bot):
    bot.add_cog(DcCogs(bot))