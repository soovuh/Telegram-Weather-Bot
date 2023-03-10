from aiogram.utils import executor
from create_bot import dp
from data_base import postgres_db
from handlers import client, registration, get_location
from time_control import time_control
import asyncio

# when bot starts, we want to see, that he start, and connect db
# You can also use sqlite_db, for this you need replace in all file postgres_db on sqlite_db and
# use "from data_base import sqlite_db".


async def on_startup(_):
    print('Bot started!')
    postgres_db.sql_start()
    asyncio.create_task(time_control.check_time())

# register handlers
client.register_handlers_client(dp)
registration.register_handlers_registration(dp)
get_location.register_handlers_get_location(dp)

# start checking for messages
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
