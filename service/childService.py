from service.dbService import DatabaseService


def gera_queryset(args):
    query = {"query": "", }
    args = [arg.lower() for arg in args]

    for arg in args:
        if arg in ("water", "fire", "forest", "dark", "light"):
            query['element'] = arg
        elif arg in ("attacker", "debuffer", "tank", "healer", "support"):
            query['role'] = arg
        elif arg in ("5", "4", "3"):
            query['rank'] = arg
        else:
            query['query'] = query['query'] + arg
    return query


class ChildService(DatabaseService):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def find_all(self):
        return await self.fetch("SELECT * from childs")

    async def list_all_keywords(self):
        return await self.fetch("SELECT child_call, alias1, alias2, name FROM childs")

    async def find_one_similar(self, child_call: str):
        child_call = child_call.lower()

        row = await self.fetchrow("SELECT * FROM childs where similarity($1, child_call) > 0.8 ORDER BY \
         $1 <-> child_call LIMIT 1", child_call)
        if not row:
            await self.fetchrow("SELECT * FROM childs WHERE similarity($1, alias1) > 0.8 ORDER BY \
             $1 <-> alias1 LIMIT 1", child_call)
        if not row:
            await self.fetchrow("SELECT * FROM childs WHERE similarity($1, alias2) > 0.8 ORDER BY \
             $1 <-> alias2 LIMIT 1", child_call)

        return row if row else None

    async def find_five_similar(self, child_call: str):
        child_call = child_call.lower()
        rows = await self.fetch("select * from childs where similarity($1, child_call) > 0.3 or similarity($1, alias1) \
         > 0.3 or similarity($1, alias2) > 0.3 order by $1 <-> child_call LIMIT 5", child_call)
        return rows

    async def find_similar_list(self, query):
        return await self.fetch("SELECT * FROM childs WHERE concat(child_call, alias1, alias2, name) similar to $1;",
                                f"%{query}%")

    async def find_list_units(self, args):
        query_set = gera_queryset(args)
        records = await self.find_similar_list(query_set['query']) if query_set[
                                                                          'query'] != "" else await self.find_all()

        if 'element' in query_set:
            records = [record for record in records if record['element'].lower() == query_set['element']]
        if 'role' in query_set:
            records = [record for record in records if record['role'].lower() == query_set['role']]
        if 'rank' in query_set:
            records = [record for record in records if record['rank'].lower() == query_set['rank']]
        return records
