from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# This is creating cancel inline keyboard

b1 = InlineKeyboardButton(text='Відміна', callback_data='/rollback2')

cancel_kb_2 = InlineKeyboardMarkup(row_width=1)

cancel_kb_2.add(b1)
