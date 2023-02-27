import sqlite3 as sq
from create_bot import Bot
from weather import weather_search
from create_bot import bot
from inline_buttons import client_kb

# function for connect to database, and create table users if not exist
def sql_start():
    global base, cur
    base = sq.connect('weather_db.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('''
                CREATE TABLE IF NOT EXISTS
                users(user_id, city_name, lat, lon, alert_time, just_for)
                 ''')
    base.commit()

# adding city and user_id in database or updating info about city if user_id already exists in table
async def sql_add_command(state, ID):
    async with state.proxy() as data:
        if data.get('lat') and data.get('lon'):
            lat, lon = data.get('lat'), data.get('lon')
            city = await weather_search.get_city(lat, lon)
            if city:
                city = await weather_search.translate_to_ua(city)
                check = cur.execute(f'''
                                    SELECT city_name FROM users WHERE user_id = {ID}
                                    ''').fetchone()
                if check != None:
                    cur.execute('''
                                UPDATE users
                                SET lat = ?, lon = ?
                                WHERE user_id = ?
                                ''', (lat, lon, ID))
                    base.commit()
                    cur.execute('''
                                UPDATE users
                                SET city_name = ?
                                WHERE user_id = ?
                                ''', (city, ID))
                    base.commit()
                else:
                    cur.execute('''
                                INSERT INTO users(lat, lon, city_name, user_id, just_for)
                                VALUES(?, ?, ?, ?, ?, ?)
                                ''', (lat, lon, city, ID, 'morning', True))
                    base.commit()
            else:
                await bot.send_message(ID, 'Сталася помилка, спробуйте ще раз або трохи пізніше', reply_markup=client_kb)
                
        elif data.get('city'):
            city = data.get('city')
            city = await weather_search.translate_to_ua(city)
            cords = await weather_search.get_cords(city)
            lat, lon = cords
            if lat and lon:
                check = cur.execute(f'''
                                    SELECT city_name FROM users WHERE user_id = {ID}
                                    ''').fetchone()
                if check != None:
                    cur.execute('''
                                UPDATE users
                                SET city_name = ?
                                WHERE user_id = ?
                                ''', (city, ID))
                    base.commit()
                    cur.execute('''
                                UPDATE users
                                SET lat = ?, lon = ?
                                WHERE user_id =?
                                ''', (lat, lon, ID))
                    base.commit()
                else:
                    cur.execute('''
                                INSERT INTO users(city_name, user_id, lat, lon, alert_time, just_for)
                                VALUES(?, ?, ?, ?, ?, ?)
                                ''', (city, ID, lat, lon, 'morning', True))
                    base.commit()
            else:
                await bot.send_message(ID, 'Сталася помилка, спробуйте ще раз, або трохи пізніше', reply_markup=client_kb)


# get coords from user_id
async def sql_get_coords(ID):
    cords = cur.execute(f'''
                        SELECT lat, lon FROM users WHERE user_id = {ID}
                        ''').fetchone()
    return cords

async def sql_get_city(ID):
    city = cur.execute(f'''
                        SELECT city_name FROM users WHERE user_id = {ID}
                       ''').fetchone()[0]

    return city

async def check_user(ID):
    check = cur.execute(f'SELECT user_id FROM users WHERE user_id = {ID}').fetchone()
    return True if check else False
    

async def add_alert_time(ID, alert_time):
    check = await check_user(ID)
    if check:
        cur.execute(f'''
                    UPDATE users
                    SET alert_time = ?
                    WHERE user_id = ?
                    ''', (alert_time, ID))
        base.commit()
        return True
    else:
        return False

async def delete_alert(ID):
    check = await check_user(ID)
    if check:
        cur.execute(f'''
                    UPDATE users
                    SET alert_time = ?
                    WHERE user_id = ?
                    ''', ('None', ID))
        base.commit()
        return True
    else:
        return False 

async def get_users_to_alert(alert_time):
    users_list = cur.execute(f'''
                        SELECT user_id
                        FROM users
                        WHERE alert_time = ? AND just_for = ?
                        ''', (alert_time, True)).fetchall()
    users = []
    for user in users_list:
        users.append(user[0])
    print(users)
    return users
