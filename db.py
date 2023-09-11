import sqlite3
import logging

database = sqlite3.connect("db.db")
cursor = database.cursor()

try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        username TEXT,
        input BOOLEAN DEFAULT True,
        input_data TEXT,
        name TEXT,
        family_name TEXT,
        phone TEXT,
        phone_verified BOOLEAN DEFAULT False,
        country TEXT,
        country_verified BOOLEAN,
        email TEXT,
        role TEXT,
        checked_in BOOLEAN DEFAULT False,
        settings BOOLEAN DEFAULT True,
        addresses TEXT,
        orders_filter TEXT,
        responses_filter TEXT,
        payment_form TEXT,
        bank TEXT,
        account TEXT
    )''')
except Exception as ex:
    logging.error(f'Users table already exists. {ex}')


try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer TEXT,
        seller TEXT,
        status TEXT,
        approved_by TEXT,
        reason TEXT,
        address TEXT,
        name TEXT,
        photo TEXT,
        comment TEXT,
        country TEXT,
        link TEXT,
        notified TEXT,
        response_id INTEGER,
        payment_photo TEXT,
        transfer_photo TEXT
    )''')

except Exception as ex:
    logging.error(f'Orders table already exists. {ex}')


try:
    # creates table with new users and their referrals
    cursor.execute('''CREATE TABLE responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        name TEXT,
        seller TEXT,
        price REAL,
        delivery BOOLEAN,
        comment TEXT,
        status TEXT,
        buyer TEXT,
        payment_form TEXT,
        bank TEXT,
        account TEXT
    )''')
except Exception as ex:
    logging.error(f'Responses table already exists. {ex}')

# cursor.execute("DELETE FROM referrals WHERE id<>1000")
# database.commit()