from aiogram import types, Dispatcher
from create_bot import dp, bot
from inline_buttons import client_kb, alert_kb
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


async def choose_alert_time(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Виберіть час, коли ви хочете отримувати сповіщення про погоду', reply_markup=alert_kb)
    await callback.answer('Меню оповіщень...')


async def morning_alert(callback: types.CallbackQuery):
    check = await sqlite_db.add_alert_time(callback.from_user.id, 'morning')
    if check:
        await callback.answer('Готово!')
        await bot.send_message(callback.from_user.id,'Зміни збережені', reply_markup=client_kb)
    else:
        await bot.send_message(callback.from_user.id, 'Спочатку треба зарээструватися!', reply_markup=client_kb)
        await callback.answer('Помилка!') 


async def noon_alert(callback: types.CallbackQuery):
    check = await sqlite_db.add_alert_time(callback.from_user.id, 'noon')
    if check:
        await callback.answer('Готово!')
        await bot.send_message(callback.from_user.id,'Зміни збережені', reply_markup=client_kb)
    else:
        await bot.send_message(callback.from_user.id, 'Спочатку треба зарээструватися!', reply_markup=client_kb)
        await callback.answer('Помилка!')


async def evening_alert(callback: types.CallbackQuery):
    check = await sqlite_db.add_alert_time(callback.from_user.id, 'evening')
    if check:
        await bot.send_message(callback.from_user.id,'Зміни збережені', reply_markup=client_kb)
        await callback.answer('Готово!')
    else:
        await bot.send_message(callback.from_user.id, 'Спочатку треба зарээструватися!', reply_markup=client_kb)
        await callback.answer('Помилка!')


async def cancel_alert(callback: types.CallbackQuery):
    check = await sqlite_db.delete_alert(callback.from_user.id)
    if check:
        await bot.send_message(callback.from_user.id,'Зміни збережені', reply_markup=client_kb)
        await callback.answer('Готово!')
    else:
        await bot.send_message(callback.from_user.id, 'Спочатку треба зарээструватися!', reply_markup=client_kb)
        await callback.answer('Помилка!')


async def send_alert(alert_time):
    users_id = await sqlite_db.get_users_to_alert(alert_time)
    for user_id in users_id:
        check_user = await sqlite_db.check_user(user_id)
        if check_user:
            city = await sqlite_db.sql_get_city(user_id)
            cords = await sqlite_db.sql_get_coords(user_id)
            lat, lon = cords

            if not lat or not lon or not city:
                await bot.send_message(user_id, 'Спочатку треба вказати місце для отримання погоди!', reply_markup=client_kb)
            else:
                weather_info, weather_icon = await weather_search.get_weather(lat, lon, city)
                await bot.send_photo(user_id, photo=weather_icon, caption = weather_info, reply_markup=client_kb)
        else:
            await bot.send_message(user_id, 'Спочатку треба встановити місцезнаходження!', reply_markup=client_kb)

# registration handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_commands, commands=['start'])
    dp.register_callback_query_handler(info_command, text='/info')
    dp.register_callback_query_handler(
        see_weather_now, text='/weather_in_my_city_now')
    dp.register_callback_query_handler(choose_alert_time, text='/set_alert_time')
    dp.register_callback_query_handler(morning_alert, text='/morning')
    dp.register_callback_query_handler(noon_alert, text='/noon')
    dp.register_callback_query_handler(evening_alert, text='/evening')
    dp.register_callback_query_handler(cancel_alert, text='/delete_alert')
