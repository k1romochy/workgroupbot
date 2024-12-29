from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Все документы')], [KeyboardButton(text='Висяки')], [KeyboardButton(text='Команды')]],
                           resize_keyboard=True)

commands = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить документы')], [KeyboardButton(text='Все документы')], [KeyboardButton(text='Висяки')],
    [KeyboardButton(text='Шаблон')], [KeyboardButton(text='Удалить все документы')]
], resize_keyboard=True)
