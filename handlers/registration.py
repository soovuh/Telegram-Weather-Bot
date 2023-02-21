from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot
from inline_buttons import cancel_kb, client_kb


class FSMRegistration(StatesGroup):
    city = State()


async def cm_start(callback: types.CallbackQuery):
    await FSMRegistration.city.set()
    await bot.send_message(callback.from_user.id, 'Напишите свой город', reply_markup=cancel_kb)  
    
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(callback.from_user.id, 'Откат', reply_markup=client_kb)