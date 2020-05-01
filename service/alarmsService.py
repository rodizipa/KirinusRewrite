from service.dbService import DatabaseService


class AlarmService(DatabaseService):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot

    async def get_alarm(self, name):
        return await self.fetchrow("SELECT * FROM alarms WHERE $1 = alarm_name;", name)

    async def update_alarm(self, alarm, time):
        await self.execute("UPDATE alarms SET alarm_time = $1  WHERE alarm_name = $2;", time, alarm)

    async def insert_alarm(self, alarm, time):
        await self.execute("INSERT INTO alarms (alarm_name, alarm_time) VALUES ($1, $2);", alarm, time)
