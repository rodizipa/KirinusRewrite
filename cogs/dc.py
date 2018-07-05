from discord.ext import commands
from utils.formatter import element_color
from discord import Embed
import datetime

class DcCogs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='raid')
    async def raid(self, ctx, *args):
        """Call raids announcement."""
        if ctx.message.channel.id == 167280538695106560 or ctx.message.channel.id == 449061137523277834:
            m = await ctx.send("@here")

            # Set raid owner
            if ctx.message.mentions:
                owner = ctx.message.mentions[0].display_name
            else:
                owner = ctx.author.display_name

            # default raid alert
            em = Embed(colour=await element_color('Light'), title="Raid Alert!", description=f"@here, {owner} found a raid!", timestamp=datetime.datetime.now())
            em.set_image(url="https://cdn.discordapp.com/attachments/242845451739463681/418594680528437278/something_smaller.png")

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
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438365216899085/hildr.png")

                elif raid_call in 'neman':
                    em.colour = await element_color('Dark')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438463892226068/Neman.png")

                elif raid_call == 'nicole':
                    em.colour = await element_color('Forest')
                    em.description = f'@here, {owner} found a {raid_call}!'
                    em.set_image(url="https://cdn.discordapp.com/attachments/167280538695106560/422438410498736148/nicole.png")

                else:
                    em.description = f'@here, {owner} found a/an {raid_call}'

            if level:
                em_edit = em.description
                em.description = em_edit + f"\nAlso, appears to be lvl **{level}**.\n"

            await m.delete()
            await ctx.send(embed=em)
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            await ctx.author.send("You can't do raid call outside of raid channel.")


def setup(bot):
    bot.add_cog(DcCogs(bot))