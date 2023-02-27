from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Так', callback_data='/send_joke_true')
b2 = InlineKeyboardButton(text='Ні', callback_data='/send_joke_false')

joke_kb = InlineKeyboardMarkup(row_width=2)
joke_kb.row(b1, b2)
