from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Поділитись локацією', callback_data='/register_loc')
b2 = InlineKeyboardButton(text='Написати місто власноруч', callback_data='/register_city')

choose_kb = InlineKeyboardMarkup(row_width=2)
choose_kb.row(b1, b2)


