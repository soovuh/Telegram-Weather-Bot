import psycopg2 as pg
from create_bot import Bot
from weather import weather_search
from create_bot import bot
from inline_buttons import client_kb
from config import my_db_password

# function for connect to database, and create table users if not exist


def sql_start():
    global base, cur
    base = pg.connect(
        host='localhost',
        database='weather_db',
        user='postgres',
        password=my_db_password
    )
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    cur.execute('''
                CREATE TABLE IF NOT EXISTS
                users(user_id INTEGER, city_name varchar(255), 
                lat double precision, lon double precision, 
                alert_time varchar(255), just_for boolean, 
                send_joke boolean DEFAULT true)
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
                                    ''')

                check = cur.fetchone()
                if check != None:
                    cur.execute('''
                                UPDATE users
                                SET lat = %s, lon = %s
                                WHERE user_id = %s
                                ''', (lat, lon, ID))
                    base.commit()
                    cur.execute('''
                                UPDATE users
                                SET city_name = %s
                                WHERE user_id = %s
                                ''', (city, ID))
                    base.commit()
                else:
                    cur.execute('''
                                INSERT INTO users(lat, lon, city_name, user_id, just_for)
                                VALUES(%s, %s, %s, %s, %s, %s)
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
                                    ''')

                check = cur.fetchone()
                if check != None:
                    cur.execute('''
                                UPDATE users
                                SET city_name = %s
                                WHERE user_id = %s
                                ''', (city, ID))
                    base.commit()
                    cur.execute('''
                                UPDATE users
                                SET lat = %s, lon = %s
                                WHERE user_id = %s
                                ''', (lat, lon, ID))
                    base.commit()
                else:
                    cur.execute('''
                                INSERT INTO users(city_name, user_id, lat, lon, alert_time, just_for)
                                VALUES(%s, %s, %s, %s, %s, %s)
                                ''', (city, ID, lat, lon, 'morning', True))
                    base.commit()
            else:
                await bot.send_message(ID, 'Сталася помилка, спробуйте ще раз, або трохи пізніше', reply_markup=client_kb)


# get coords from user_id
async def sql_get_coords(ID):
    cords = cur.execute(f'''
                        SELECT lat, lon FROM users WHERE user_id = {ID}
                        ''')
    cords = cur.fetchone()
    return cords


async def sql_get_city(ID):
    city = cur.execute(f'''
                        SELECT city_name FROM users WHERE user_id = {ID}
                       ''')
    city = cur.fetchone()[0]

    return city


async def check_user(ID):
    check = cur.execute(
        'SELECT user_id FROM users WHERE user_id = %s AND just_for = %s',
        (ID, True))
    check = cur.fetchone()
    return True if check else False


async def add_alert_time(ID, alert_time):
    check = await check_user(ID)
    if check:
        cur.execute('''
                    UPDATE users
                    SET alert_time = %s
                    WHERE user_id = %s
                    ''', (alert_time, ID))
        base.commit()
        return True
    else:
        return False


async def delete_alert(ID):
    check = await check_user(ID)
    if check:
        cur.execute('''
                    UPDATE users
                    SET alert_time = %s
                    WHERE user_id = %s
                    ''', ('None', ID))
        base.commit()
        return True
    else:
        return False


async def get_users_to_alert(alert_time):
    users_list = cur.execute('''
                        SELECT user_id
                        FROM users
                        WHERE alert_time = %s AND just_for = %s
                        ''', (alert_time, True))
    users_list = cur.fetchall()
    if users_list != []:
        users = []
        for user in users_list:
            users.append(user[0])
        return users
    return False


async def get_users_to_send_joke(alert_time):
    users_list = cur.execute('''
                            SELECT user_id
                            FROM users
                            WHERE alert_time = %s AND send_joke = %s
                            ''', (alert_time, True))
    users_list = cur.fetchall()
    if users_list != []:
        users = []
        for user in users_list:
            users.append(user[0])
        return users
    return False


async def send_joke_status(ID, status):
    check = await check_user(ID)
    if check:
        cur.execute('''
                    UPDATE users
                    SET send_joke = %s
                    WHERE user_id = %s
                    ''', (status, ID))
        base.commit()
        return True
    else:
        return False
