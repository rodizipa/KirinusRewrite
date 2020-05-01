import datetime

from service.dbService import DatabaseService


class QuoteService(DatabaseService):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def find_all(self):
        return await self.fetch("SELECT invoke FROM quotes")

    async def find_one(self, invoke):
        return await self.fetchrow("SELECT * FROM quotes WHERE $1 = invoke;", invoke)

    async def update_quote(self, ctx, args):
        await self.execute("UPDATE quotes SET text = $1, created_at = $2, user_id = $3, created_by = \
         $4 WHERE invoke = $5;", args[2], datetime.datetime.now(), ctx.author.id, ctx.author.display_name, args[1])

    async def insert_quote(self, ctx, args):
        await self.execute("INSERT INTO quotes (invoke, text, created_by, created_at, user_id) VALUES \
         ($1, $2, $3, $4, $5);", args[1], args[2], ctx.author.name, datetime.datetime.now(), ctx.author.id)

    async def delete_quote(self, invoke):
        await self.execute("DELETE FROM quotes WHERE invoke = $1", invoke)
