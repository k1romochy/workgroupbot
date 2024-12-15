from aiogram import Dispatcher
from dotenv import load_dotenv
from app.context import bot
import os
import asyncio

from user.handler import router as user_router
from document.handler import router as document_router
from core.models.db_helper import async_main


async def main():
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(document_router)
    await async_main()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

