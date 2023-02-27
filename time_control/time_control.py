import asyncio
import datetime
from handlers.client import send_alert

async def check_time():
    while True:
        now = datetime.datetime.now().time()

        if now.hour == 8 and now.minute == 00:
            await send_alert('morning')
        elif now.hour == 12 and now.minute == 00:
            await send_alert('noon')
        elif now.hour == 20 and now.minute == 00:
            await send_alert('evening')
        await asyncio.sleep(60)
        
