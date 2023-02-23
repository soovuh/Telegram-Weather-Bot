from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from inline_buttons import cancel_kb_2, client_kb, choose_kb
from data_base import sqlite_db

class FSMRegistrationLocation(StatesGroup):
    location = State()


# start 
async def cm_start_loc(callback: types.CallbackQuery):
    await FSMRegistrationLocation.location.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location_button = types.KeyboardButton('Share Location', request_location=True)
    keyboard.add(location_button)
    await bot.send_message(callback.from_user.id, 'Для відміни натисніть', reply_markup=cancel_kb_2)
    await bot.send_message(callback.from_user.id, 'Натисніть на кнопку "Share Location"', reply_markup=keyboard)
    await callback.answer('Ok!')

# cancel for state
async def cancel_handler_2(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(callback.from_user.id, 'Відмніа', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(callback.from_user.id, 'Меню', reply_markup=client_kb)
    await callback.answer('Відміна')


# loading city and user_id, after call sqlite_db function to save result and finish state
async def load_location(message: types.Message, state: FSMContext):
    print('alo')
    async with state.proxy() as data:
        data['location'] = message.location
    print(data['location'])
    await bot.send_message(message.from_user.id, 'Готово', reply_markup=client_kb)
    await state.finish()


# registration handlers
def register_handlers_get_location(dp: Dispatcher):
    dp.register_callback_query_handler(cm_start_loc, text='/register_loc', state=None)
    dp.register_callback_query_handler(
        cancel_handler_2, state="*", text='/rollback2')
    dp.register_message_handler(load_location, state=FSMRegistrationLocation.location)