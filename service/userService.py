from service.dbservice import DatabaseService


class UserService(DatabaseService):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def adduser(self, discord_id):
        await self.execute("insert into member(discord_id) VALUES ($1)", discord_id)

    async def getuser(self, discord_id):
        return await self.fetchrow("select * from member where discord_id = $1", discord_id)

    async def addkarma(self, discord_id, value):
        await self.execute("UPDATE member SET karma = karma + $2 where discord_id = $1", discord_id, value)

    async def userbalance(self,discord_id):
        return await self.fetchrow("select karma from member where discord_id = $1", discord_id)

    async def removekarma(self, discord_id, value):
        await self.execute("UPDATE member SET karma = karma - $2 WHERE discord_id = $1", discord_id, value)