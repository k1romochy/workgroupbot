import os

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.document import Document
import document.crud as document

import markups.main as kb

from app.context import bot

router = Router()

load_dotenv()
token = os.getenv('TOKEN')


@router.message(F.text == 'Все документы')
async def get_documents(message: Message):
    documents_url = await document.get_documents_url()

    for doc_url in documents_url:
        doc_name = await document.get_name_doc_by_url(doc_url)
        doc_id = await document.get_doc_id_by_url(doc_url)

        builder = InlineKeyboardBuilder()
        builder.button(text='Удалить', callback_data=f'del_{doc_id}')
        builder.button(text='Продлить', callback_data=f'addtime_{doc_id}')

        builder.adjust(3)
        keyboard = builder.as_markup()

        await message.answer(text=f'{doc_name}\n{doc_url}', reply_markup=keyboard)


@router.message(F.document)
async def save_document(message: Message, bot=bot):
    try:
        file = await bot.get_file(message.document.file_id)
        file_path = file.file_path
        file_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
        file_name = message.document.file_name
        document_type = message.text

        await document.add_document(url=file_url, tg_id=message.from_user.id, name=file_name, term=document_type)
        await message.reply("Документ успешно сохранён!")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


@router.callback_query(F.data.startswith('del_'))
async def del_document(callback: CallbackQuery):
    document_id = callback.data.split("del_")[1]

    await document.del_document_by_id(document_id)
    await callback.message.answer('Документ удалён')
    await callback.answer()
