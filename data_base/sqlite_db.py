import sqlite3 as sq
from create_bot import Bot

# function for connect to database, and create table users if not exist
def sql_start():
    global base, cur
    base = sq.connect('weather_db.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('''
                CREATE TABLE IF NOT EXISTS
                users(user_id, city_name)
                 ''')
    base.commit()

# adding city and user_id in database or updating info about city if user_id already exists in table
async def sql_add_command(state, ID):
    async with state.proxy() as data:
        check = cur.execute(f'''
                             SELECT city_name FROM users WHERE user_id = {ID}
                             ''').fetchone()
        if check != None:
            cur.execute('''
                        UPDATE users
                        SET city_name = ?
                        WHERE user_id = ?
                        ''', (tuple(data.values())[0], ID))
            base.commit()
        else:
            cur.execute('''
                         INSERT INTO users(city_name, user_id)
                         VALUES(?, ?)
                         ''', tuple(data.values()))
            base.commit()

# get city from user_id
async def sql_get_city(ID):
    city = cur.execute(f'''
                        SELECT city_name FROM users WHERE user_id = {ID}
                        ''').fetchone()[0]
    return city
