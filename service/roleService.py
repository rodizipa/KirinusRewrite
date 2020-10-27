import discord

from service.dbService import DatabaseService


def tratar_emote(emote):
    if isinstance(emote, str):
        return emote
    else:
        return emote.nome


class RoleService(DatabaseService):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def fetch_member_role(self, member: discord.Member, role_name: str):
        return discord.utils.get(member.roles, id=await self.get_role_id_by_name(role_name))

    async def get_role_id_by_name(self, role_name: str):
        role = await self.fetchrow("SELECT * FROM roles WHERE role_name = $1;", role_name)
        return role['role_discord_id']

    async def find_reaction_role(self, emote):
        emote = tratar_emote(emote)
        return await self.fetchrow("SELECT * FROM reaction_role WHERE emote = $1;", emote)

    async def add_reaction_role(self, emote, role):
        emote = tratar_emote(emote)
        await self.execute("INSERT INTO reaction_role (emote, role) VALUES ($1, $2)", emote, role.id)

    async def update_reaction_role(self, emote, role):
        emote = tratar_emote(emote)
        await self.execute("UPDATE reaction_role SET role = $2 WHERE emote = $1", emote, role.id)

    async def remove_reaction_role(self, emote):
        emote = tratar_emote(emote)
        await self.execute("DELETE FROM reaction_role WHERE emote = $1", emote)
