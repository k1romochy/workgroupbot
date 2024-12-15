from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Все документы')], [KeyboardButton(text='Висяки')]],
                           resize_keyboard=True)
