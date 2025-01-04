from aiogram import Dispatcher
from run.context import bot
import asyncio

from user.handler import router as user_router
from document.handler import router as document_router
from core.models.db_helper import async_main
from core.google_sheets import export_to_google_sheets


async def periodic_google_sheets_update():
    while True:
        print('aaa')
        try:
            await export_to_google_sheets()
            print("Данные успешно экспортированы в Google Таблицу")
        except Exception as e:
            print(f"Ошибка при экспорте: {e}")
        await asyncio.sleep(5) #перерыв


async def main():
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(document_router)

    await async_main()
    await export_to_google_sheets()

    asyncio.create_task(periodic_google_sheets_update())

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
