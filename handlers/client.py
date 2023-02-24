from aiogram import types, Dispatcher
from create_bot import dp, bot
from inline_buttons import client_kb
from data_base import sqlite_db
from weather import weather_search


# start command
async def start_commands(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Вітаю!', reply_markup=client_kb)
        await message.delete()
    except:
        await message.reply(
            'Для спілкування з ботом напишіть у приватні повідомлення:\nhttps://t.me/weather_soovuh_bot'
        )


# info command
async def info_command(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id,
                           '''
        Я бот, і я надсилаю погоду
        ''',
                           reply_markup=client_kb)
    await callback.answer('Окей!')


# command that translate weather in user-city in right now
async def see_weather_now(callback: types.CallbackQuery):
    await callback.answer('Шукаємо актуальну інформацію...')
    check_user = await sqlite_db.check_user(callback.from_user.id)
    if check_user:
        city = await sqlite_db.sql_get_city(callback.from_user.id)
        cords = await sqlite_db.sql_get_coords(callback.from_user.id)
        lat, lon = cords
        
        if not lat or not lon or not city:
            await bot.send_message(callback.from_user.id, 'Спочатку треба вказати місце для отримання погоди!', reply_markup=client_kb)
        else:
            weather_info, weather_icon = await weather_search.get_weather(lat, lon, city)
            
            await bot.send_photo(callback.from_user.id, photo=weather_icon,  caption=weather_info, reply_markup=client_kb)
    else:
        await bot.send_message(callback.from_user.id, 'Спочатку треба встановити місцезнаходження!', reply_markup=client_kb)


# registration handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_commands, commands=['start'])
    dp.register_callback_query_handler(info_command, text='/info')
    dp.register_callback_query_handler(
        see_weather_now, text='/weather_in_my_city_now')
