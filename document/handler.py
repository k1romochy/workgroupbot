import os

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.document import Document
import document.crud as document

import markups.kb as kb

from run.context import bot

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

        document_type = ''
        document_term = 0
        document_register = file_name.split('_')[0] + '_' + file_name.split('_')[1] + '_' + file_name.split('_')[2]

        if file_name.split('_')[3].lower() == 'ж-ба' or 'жалоба':
            document_type = 'жалоба'
            document_term = 3
        elif file_name.split('_')[3].lower() == 'х-во' or 'ходатайство':
            document_type = 'ходатайство'
            document_term = 3
        elif file_name.split('_')[3].lower() == 'заявление':
            document_type = 'заявление'
            document_term = 30

        await document.add_document(url=file_url, tg_id=message.from_user.id, name=file_name,
                                    type=document_type, term=document_term, registrated_at=document_register)
        await message.reply("Документ успешно сохранён!")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


@router.callback_query(F.data.startswith('del_'))
async def del_document(callback: CallbackQuery):
    document_id = int(callback.data.split("del_")[1])

    await document.del_document_by_id(document_id)
    await callback.message.answer('Документ удалён')
    await callback.answer()


@router.callback_query(F.data.startswith('addtime_'))
async def add_time(callback: CallbackQuery):
    document_id = int(callback.data.split('addtime_')[1])

    builder = InlineKeyboardBuilder()
    for _ in range(1, 10):
        builder.button(text=f'{_}', callback_data=f'addtimes_{document_id}_{_}')

    builder.adjust(5)
    keyboard = builder.as_markup()

    await callback.message.answer(text='На сколько дней вы хотите продлить срок документа?', reply_markup=keyboard)
    await callback.answer()


@router.message(Command('update'))
async def update_documents(message: Message):
    await document.update_documents()
    await message.answer('Вы обновили все документы')


@router.message(F.text == 'Шаблон')
async def get_clishe_for_file(message: Message):
    await message.reply('Шаблон файла: xx_xx_xx_ВИД-ДОКУМЕНТА_НАЗВАНИЕ')


@router.message(Command('deletealldoc'))
async def delete_all_docs(message: Message):
    await document.delete_all_docs()
    await message.answer('Вы успешно удалили все документы')
