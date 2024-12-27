from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from markups.kb import main
import user.crud as user

router = Router()


@router.message(Command('start'))
async def start_command(message: Message):
    await user.create_user(tg_id=message.from_user.id)

    await message.answer('Добро пожаловать!', reply_markup=main)
