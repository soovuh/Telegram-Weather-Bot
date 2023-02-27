import asyncio
import datetime
from handlers.client import send_alert
from handlers.client import send_jokes

async def check_time():
    while True:
        now = datetime.datetime.now().time()

        if now.hour == 8 and now.minute == 0:
            await send_alert('morning')
            await send_jokes('morning')
        elif now.hour == 14 and now.minute == 0:
            await send_alert('noon')
            await send_jokes('noon')
        elif now.hour == 17 and now.minute == 55:
            await send_alert('evening')
            await send_jokes('evening')
        await asyncio.sleep(60)
        
