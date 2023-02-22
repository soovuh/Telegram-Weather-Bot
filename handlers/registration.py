from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from inline_buttons import cancel_kb, client_kb
from data_base import sqlite_db


# creating class for memory
class FSMRegistration(StatesGroup):
    city = State()


# start 
async def cm_start(callback: types.CallbackQuery):
    await FSMRegistration.city.set()
    await bot.send_message(callback.from_user.id, 'Напишіть своє місто', reply_markup=cancel_kb)
    await callback.answer('Okей!')


# cancel for state
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(callback.from_user.id, 'Відкат', reply_markup=client_kb)
    await callback.answer('Відміна')


# loading city and user_id, after call sqlite_db function to save result and finish state
async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
        data['user_id'] = message.from_user.id

    await sqlite_db.sql_add_command(state, message.from_user.id)
    await bot.send_message(message.from_user.id, 'Готово', reply_markup=client_kb)
    await state.finish()


# registration handlers
def register_handlers_registration(dp: Dispatcher):
    dp.register_callback_query_handler(cm_start, text='/register', state=None)
    dp.register_callback_query_handler(
        cancel_handler, state="*", text='/rollback')
    dp.register_message_handler(load_city, state=FSMRegistration.city)
