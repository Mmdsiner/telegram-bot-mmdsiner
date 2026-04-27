import aiosqlite

DB_NAME = "bot.db"

async def execute(query, *args):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(query, args)
        await db.commit()

async def fetch(query, *args):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(query, args)
        rows = await cursor.fetchall()
        return rows
