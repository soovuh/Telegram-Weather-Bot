from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# This is creating client inline keyboard

b1 = InlineKeyboardButton(text='О 8 ранку', callback_data='/morning')
b2 = InlineKeyboardButton(text='О 14 вдень', callback_data='/noon')
b3 = InlineKeyboardButton(text='О 8 вечора', callback_data='/evening')
b4 = InlineKeyboardButton(text='Вимкнути сповіщення', callback_data='/delete_alert')
b5 = InlineKeyboardButton(text='Вимкнути анекдоти', callback_data='/send_joke_false')
b6 = InlineKeyboardButton(text='Увімкнути анекдоти', callback_data='/send_joke_true')

alert_kb = InlineKeyboardMarkup(row_width=1)

alert_kb.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)