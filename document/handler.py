import os

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.document import Document
import document.crud as document

from app.context import bot

router = Router()

load_dotenv()
token = os.getenv('TOKEN')


@router.message(F.text == 'Все документы')
async def get_documents(message: Message):
    documents = await document.get_documents_url()

    for doc in documents:
        await message.answer(text=doc)


@router.message(F.document)
async def save_document_handler(message: Message, bot=bot):
    try:
        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path
        file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"

        await document.add_document(url=file_url, tg_id=message.from_user.id)
        await message.reply("Документ успешно сохранён!")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")



