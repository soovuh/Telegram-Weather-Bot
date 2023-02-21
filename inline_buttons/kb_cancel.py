from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

b1 = InlineKeyboardButton(text='Отмена', callback_data='/rollback')

cancel_kb = InlineKeyboardMarkup(row_width=1)

cancel_kb.add(b1)