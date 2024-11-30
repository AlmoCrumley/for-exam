import aiosqlite

DATABASE_NAME = 'questions.db'


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        await db.commit()


async def add_question(question: str, answer: str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('INSERT INTO questions (question, answer) VALUES (?, ?)', (question, answer))
        await db.commit()

async def get_all_questions():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('SELECT * FROM questions') as cursor:
            return await cursor.fetchall()

async def get_question_by_id(question_id: int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('SELECT * FROM questions WHERE id = ?', (question_id,)) as cursor:
            return await cursor.fetchone()