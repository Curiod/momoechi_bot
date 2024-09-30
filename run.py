import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.database.main_database import create_tables

from app.handlers import router


async def main():
    await create_tables()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')