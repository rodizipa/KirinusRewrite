from discord.ext import commands
import discord
import asyncio


class AdminCog:
    """Owner and Admin Stuff"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='role')
    @commands.is_owner()
    async def role(self, ctx, action, user: discord.Member, result_role: discord.Role):
        """Assign/remove roles to user."""
        if action == 'add':
            await user.add_roles(result_role)
            await asyncio.sleep(1)
            await ctx.message.delete()

        elif action == 'remove':
            await user.remove_roles(result_role)
            await asyncio.sleep(1)
            await ctx.message.delete()

    @commands.command(name='nick')
    @commands.is_owner()
    async def change_nick(self,ctx, user: discord.Member, nick):
        """Change target nickname"""
        await user.edit(nick=nick)
        await ctx.message.delete()

    @commands.command(name='purge', aliases=['prune'])
    @commands.is_owner()
    async def purge(self,ctx, number: int):
        """Purge chat by x."""
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=number)

    @commands.command(name="inquisition")
    @commands.is_owner()
    async def inquisition(self,ctx,action):
        """Find/burn usernames without role afk for 30 days or more."""
        if action == 'find':
            heretics = await ctx.message.guild.estimate_pruned_members(days=30)
            await ctx.send(f'{heretics} heretics found during the brazilian inquisition.')
        elif action =='burn':
            heretics = await ctx.message.guild.prune_members(days=30, reason="Nobody expects the brazilian inquisition.")

        await ctx.message.delete()

    @commands.command(name='say')
    @commands.is_owner()
    async def say(self, ctx, *, text:str):
        """Repeats what was typed."""
        await ctx.send(text)
        await ctx.message.delete()

    @commands.command(name='listreact')
    @commands.is_owner()
    async def listreact(self, ctx, channel: discord.TextChannel, target_id: int):
        if target_id:
            m = await channel.get_message(target_id)

            if m:
                react_list = []

                for react in m.reactions:
                    react_list.append(f"React: {str(react)}\n")
                    async for user in react.users():
                        react_list.append(f' {str(user)}\n')

                with open('reactionlist.txt','w', encoding='utf8') as f:
                    for line in react_list:
                        f.write(line)

        else:
            m = await ctx.send("No message with such ID found. (Deleted, can bot see?, missing argument?)")
            await asyncio.sleep(5)
            await m.delete()
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(AdminCog(bot))