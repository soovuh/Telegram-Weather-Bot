from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# This is creating cancel inline keyboard

b1 = InlineKeyboardButton(text='Відміна', callback_data='/rollback')

cancel_kb = InlineKeyboardMarkup(row_width=1)

cancel_kb.add(b1)