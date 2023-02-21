from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

b1 = InlineKeyboardButton(text = 'Установить мой город', callback_data='/register')

client_kb = InlineKeyboardMarkup(row_width=2)

client_kb.add(b1)