from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# This is creating client inline keyboard

b1 = InlineKeyboardButton(text='Інформація', callback_data='/info')
b2 = InlineKeyboardButton(text='Встановити моє місцезнаходження',
                          callback_data='/register')
b3 = InlineKeyboardButton(
    text='Погода зараз', callback_data='/weather_in_my_city_now')


client_kb = InlineKeyboardMarkup(row_width=2)

client_kb.row(b1, b2).row(b3)
