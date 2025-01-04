import os

from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from math import fabs

from core.models.document import Document
import document.crud as document

from markups.kb import commands


from run.context import bot

router = Router()

load_dotenv()
token = os.getenv('TOKEN')


@router.message(F.text == 'Все документы')
async def get_documents(message: Message):
    documents_url = await document.get_documents_url()

    if documents_url:
        await message.answer('Вот список всех документов:')
        for doc_url in documents_url:
            doc_name = await document.get_name_doc_by_url(doc_url)
            doc_id = await document.get_doc_id_by_url(doc_url)
            doc_time_diff = await document.get_term_diff_by_id(doc_id)

            builder = InlineKeyboardBuilder()
            builder.button(text='Удалить', callback_data=f'del_{doc_id}')
            builder.button(text='Продлить', callback_data=f'addtime_{doc_id}')
            builder.button(text='Скачать файл', url=f'{doc_url}')

            builder.adjust(2)
            keyboard = builder.as_markup()

            if doc_time_diff >= 0:
                await message.answer(text=f'{doc_name}\nПросрочится через {doc_time_diff} д.', reply_markup=keyboard)
            else:
                doc_time_diff = fabs(doc_time_diff)
                await message.answer(text=f'{doc_name}\nДокумент просрочился на {doc_time_diff} д.', reply_markup=keyboard)
    else:
        await message.answer('Пока что ничего не было сохранено')


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

        solve = document_register.split('_')

        if int(solve[0]) > 2000 and int(solve[0]) < 3000 and int(solve[1]) < 13 and int(solve[2]) < 32:
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
        else:
            await message.answer('Документ не был сохранён, так как дата написана некорректно.')
    except IntegrityError:
        await message.reply(f"Произошла ошибка, этот документ уже сохранён в базе.")
    except Exception:
        await message.reply(f'Произошла ошибка, документ не был сохранён, проверьте правильность названия файла.')


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


@router.message(F.text == 'Обновить документы')
async def update_documents(message: Message):
    await document.update_documents()
    await message.answer('Вы удалили все просроченные документы')


@router.message(F.text == 'Шаблон')
async def get_clishe_for_file(message: Message):
    await message.reply('Шаблон файла: xx_xx_xx_ВИД-ДОКУМЕНТА_НАЗВАНИЕ')


@router.message(Command('Удалить все документы'))
async def delete_all_docs(message: Message):
    await document.delete_all_docs()
    await message.answer('Вы успешно удалили все документы')


@router.callback_query(F.data.startswith('addtimes_'))
async def add_time_doc(callback: CallbackQuery):
    document_id = int(callback.data.split('addtimes_')[1].split('_')[0])
    days = int(callback.data.split('addtimes_')[1].split('_')[1])

    await document.add_time(document_id, days)
    await callback.message.answer('Вы успешно продлили срок документа')
    await callback.answer()


@router.message(F.text == 'Висяки')
async def get_prosrok_doc(message: Message):
    try:
        list_of_documents = await document.get_prosroki()

        if not list_of_documents:
            await message.answer("Нет просроченных документов.")
            return

        await message.answer('Вот все просроченные документы:')
        for doc_id, diff in list_of_documents:
            doc_name = await document.get_name_by_id(doc_id)
            doc_url = await document.get_url_by_id(doc_id)

            builder = InlineKeyboardBuilder()
            builder.button(text='Удалить', callback_data=f'del_{doc_id}')
            builder.button(text='Продлить', callback_data=f'addtime_{doc_id}')
            builder.button(text='Скачать файл', url=f'{doc_url}')

            builder.adjust(2)
            keyboard = builder.as_markup()

            text = f"{doc_name}\nПросрочено на {diff} дней."

            await message.answer(text=text, reply_markup=keyboard)
    except Exception as e:
        await message.answer(f'Что-то пошло не так: {e}')


@router.message(F.text == 'Команды')
async def get_all_commands(message: Message):
    await message.answer('Вот все доступные команды', reply_markup=commands)
    