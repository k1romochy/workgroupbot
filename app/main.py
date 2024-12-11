from aiogram import Dispatcher
from dotenv import load_dotenv
from app.context import bot
import os
import asyncio

from core.models.db_helper import async_main


async def main():
    dp = Dispatcher()
    dp.include_router(*_router)
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
