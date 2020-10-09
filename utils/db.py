import asyncio
from databases import Database

try:
    from conf import config
except:
    config = {'DSN': 'sqlite:///telegram.db'}



class DatabaseTG(Database):
    async def seed(self):
        await self.connect()
        # SQL query for sqlite
        queries = ["""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, 
                tg_id INTEGER, 
                tg_username TEXT, 
                created_at TEXT, 
                about TEXT
            );""", 
            """
            CREATE TABLE IF NOT EXISTS message_log (
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               message TEXT,
               FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );"""
        ]
        for q in queries:     
            await self.execute(q)


db = DatabaseTG(config.get('DSN'))


if __name__ == '__main__':
    asyncio.run(db.seed())
