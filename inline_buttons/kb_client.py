from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# This is creating client inline keyboard

b1 = InlineKeyboardButton(text='Інформація', callback_data='/info')
b2 = InlineKeyboardButton(text='Встановити місцезнаходження',
                          callback_data='/register')
b3 = InlineKeyboardButton(
    text='Погода зараз', callback_data='/weather_in_my_city_now')


client_kb = InlineKeyboardMarkup(row_width=1)

client_kb.add(b1).add(b2).add(b3)
