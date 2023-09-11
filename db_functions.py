import sqlite3
import telebot
import logging
import itertools
import inspect

import config

#! ДЛЯ ОБРАБОТКИ ПОЛЬЗОВАТЕЛЕЙ
#TODO Новые пользователи
def is_in_database(user_id):
    """Checks if user already in database."""

    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        users = cursor.execute(f'''SELECT COUNT(id) 
                                FROM users 
                                WHERE user_id=?
                                ''', (user_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return users
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при проверке наличия пользователя в БД ({user_id}). {ex}')


def add_user(user_id, username, name, family_name):
    """Adds a new user to database."""

    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO users (user_id, username, name, family_name, input_data, addresses, orders_filter, responses_filter)
            VALUES (?, ?, ?, ?, ?, ?, ?,?)
            ''', (user_id, username, name, family_name, 'role', '[]', 'all', 'all',))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Пользователь ({user_id} - {username}) приступил к регистрации.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при регистрации пользователя ({user_id} - {username}). {ex}')


#TODO Извлечение данных о пользователях
def get_input_status(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        users = cursor.execute(f'''SELECT input, input_data 
                                FROM users 
                                WHERE user_id=?
                                ''', (user_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return users
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить статус ввода пользователя ({user_id}). {ex}')


def get_field_info(user_id, field):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM users 
                                WHERE user_id=?
                                ''', (user_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о поле {field} пользователя ({user_id}). {ex}')


def get_users_all_info(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT *
                                FROM users 
                                WHERE user_id=?
                                ''', (user_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о пользователе ({user_id}). {ex}')


def get_interested_sellers(buyer_id, country):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        if country != '-':
            users_ids = cursor.execute(f'''SELECT user_id
                                    FROM users 
                                    WHERE user_id<>? AND role=? AND (country=? OR settings=?)
                                    ''', (buyer_id, 'seller', country, True,)).fetchall()
        else:
            users_ids = cursor.execute(f'''SELECT user_id
                                    FROM users 
                                    WHERE user_id<>? AND role=?
                                    ''', (buyer_id, 'seller',)).fetchall()

        cursor.close()
        database.close

        if users_ids:
            users_ids = itertools.chain.from_iterable(users_ids)

        return users_ids
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о пользователях для рассылки заявки. {ex}')


#TODO Внесение данных о пользователях
def update_field(user_id, field, value):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE users
                        SET {field}=?
                        WHERE user_id=?
                        ''', (value, user_id,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Поле ({field}) пользователя {user_id} изменено на {value}.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось изменить поле ({field}) пользователя {user_id} на {value}. {ex}')


#! ДЛЯ ОБРАБОТКИ ЗАЯВОК
#TODO Новая заявка
def add_order(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO orders (buyer, status, notified)
            VALUES (?, ?, ?)
            ''', (user_id, 'creating', '[]',))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Пользователь ({user_id} - приступил к созданию заявки.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при создании заявки пользователя ({user_id}). {ex}')


#TODO Извлечение данных о заявках
def select_user_orders(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        orders = cursor.execute(f'''SELECT id, name, status
                                FROM orders 
                                WHERE buyer=?
                                ORDER BY id DESC
                                ''', (user_id,)).fetchall()
        
        cursor.close()
        database.close

        return orders
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить заявки пользователя ({user_id}). {ex}')


def get_order_field_info(user_id, field):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM orders 
                                WHERE buyer=? AND (status=? OR status=?)
                                ''', (user_id, 'creating', 'created',)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о поле {field} пользователя ({user_id}). {ex}')


def get_field_info_by_order_id(order_id, field):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM orders 
                                WHERE id=?
                                ''', (order_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о поле {field} в заявке ({order_id}). {ex}')


def select_creating_orders(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        orders = cursor.execute(f'''SELECT COUNT(id) 
                                FROM orders
                                WHERE buyer=? AND (status=? OR status=?)
                                ''', (user_id, 'creating', 'created',)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return orders
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при проверке наличия у пользователя ({user_id}) заказов в стадии создания. {ex}')


def get_order_info(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        order_info = cursor.execute(f'''SELECT address, name, photo, comment, country, link 
                                FROM orders
                                WHERE buyer=? AND status=?
                                ''', (user_id, 'created',)).fetchall()[0]
        
        cursor.close()
        database.close

        return order_info

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о заказе пользователя ({user_id}). {ex}')


def get_order_info_by_order_id(order_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        order_info = cursor.execute(f'''SELECT status, reason, address, name, photo, comment, country, link
                                FROM orders 
                                WHERE id=?
                                ''', (order_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return order_info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить данные о заявке ({order_id}). {ex}')


def get_all_order_info_by_order_id(order_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        order_info = cursor.execute(f'''SELECT *
                                FROM orders 
                                WHERE id=?
                                ''', (order_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return order_info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить данные о заявке ({order_id}). {ex}')


def select_unfinished_orders_whole_world(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        orders_ids = cursor.execute(f'''SELECT id
                                FROM orders
                                WHERE buyer<>? AND status=? AND notified NOT LIKE "%'{user_id}'%"
                                ''', (user_id, 'searching',)).fetchall()
        
        cursor.close()
        database.close

        if orders_ids:
            orders_ids = itertools.chain.from_iterable(orders_ids)

        return orders_ids
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о незакрытых заявках. {ex}')


def select_unfinished_orders_location_country(user_id, country):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        orders_ids = cursor.execute(f'''SELECT id
                                FROM orders
                                WHERE buyer<>? AND status=? AND notified NOT LIKE "%'{user_id}'%" AND country=?
                                ''', (user_id, 'searching', country)).fetchall()
        
        cursor.close()
        database.close

        if orders_ids:
            orders_ids = itertools.chain.from_iterable(orders_ids)

        return orders_ids
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о незакрытых заявках. {ex}')


#TODO Обновление данных в заявке
def update_order_field(user_id, field, value):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE orders
                        SET {field}=?
                        WHERE buyer=? AND (status=? OR status=?)
                        ''', (value, user_id, 'creating', 'created',))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Поле ({field}) пользователя {user_id} изменено на {value} в таблице заявок.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось изменить поле ({field}) пользователя {user_id} на {value} в таблице заявок. {ex}')


def update_field_by_order_id(order_id, field, value):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE orders
                        SET {field}=?
                        WHERE id=?
                        ''', (value, order_id,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Поле ({field}) в заявке {order_id} изменено на {value} в таблице заявок.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось изменить поле ({field}) в заявке {order_id} на {value} в таблице заявок. {ex}')


#TODO Удаление данных
def delete_order(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            DELETE FROM orders
            WHERE buyer=? AND (status=? OR status=?)
            ''', (user_id, 'created', 'creating',))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Заявка пользователя {user_id} удалена.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при удалении заявки пользователя ({user_id}). {ex}')


#! ДЛЯ ОБРАБОТКИ ОТКЛИКОВ
#TODO Новый отклик
def add_response(order_id, seller_id, buyer_id, name, payment_from, bank, account):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            INSERT INTO responses (order_id, seller, buyer, status, name)
            VALUES (?, ?, ?, ?, ?)
            ''', (order_id, seller_id, buyer_id, 'creating', name,))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Пользователь ({seller_id}) - оставил отклик на заявку {order_id}.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при создании отклика пользователя ({seller_id}) на заявку {order_id}. {ex}')


#TODO Извлечение данных об откликах
def select_user_responses(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        orders = cursor.execute(f'''SELECT id, name, status, order_id
                                FROM responses 
                                WHERE seller=?
                                ORDER BY id DESC
                                ''', (user_id,)).fetchall()
        
        cursor.close()
        database.close

        return orders
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить отклики пользователя ({user_id}). {ex}')


def get_response_field_info(user_id, field):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM responses 
                                WHERE seller=? AND (status=? OR status=?)
                                ''', (user_id, 'creating', 'created',)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о поле {field} пользователя ({user_id}). {ex}')


def get_field_info_by_response_id(response_id, field):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        info = cursor.execute(f'''SELECT {field}
                                FROM responses 
                                WHERE id=?
                                ''', (response_id,)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию о поле {field} в отклике ({response_id}). {ex}')


def select_creating_responses(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        responses = cursor.execute(f'''SELECT COUNT(id) 
                                FROM responses
                                WHERE seller=? AND (status=? OR status=?)
                                ''', (user_id, 'creating', 'created',)).fetchall()[0][0]
        
        cursor.close()
        database.close

        return responses
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при проверке наличия у пользователя ({user_id}) откликов в стадии создания. {ex}')


def get_response_info(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        response_info = cursor.execute(f'''SELECT order_id, name, price, delivery, comment
                                FROM responses
                                WHERE seller=? AND status=?
                                ''', (user_id, 'created',)).fetchall()[0]
        
        cursor.close()
        database.close

        return response_info

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить информацию об отклике пользователя ({user_id}). {ex}')


def check_unfinished_responses(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        responses = cursor.execute(f'''SELECT COUNT(id)
                                FROM responses
                                WHERE seller=? AND status<>? AND status<>? AND status<>?
                                ''', (user_id, 'canceled', 'declined', 'done')).fetchall()[0][0]
        
        cursor.close()
        database.close

        return responses

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить данные о незавершенных откликах пользователя ({user_id}). {ex}')


def get_response_info_by_response_id(response_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        response_info = cursor.execute(f'''SELECT status, name, price, delivery, comment, order_id
                                FROM responses
                                WHERE id=?
                                ''', (response_id,)).fetchall()[0]
        
        cursor.close()
        database.close

        return response_info
    
    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось получить данные об отклике ({response_id}). {ex}')


#TODO Обновление данных в отклике
def update_response_field(user_id, field, value):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE responses
                        SET {field}=?
                        WHERE seller=? AND (status=? OR status=?)
                        ''', (value, user_id, 'creating', 'created',))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Поле ({field}) пользователя {user_id} изменено на {value} в таблице откликов.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось изменить поле ({field}) пользователя {user_id} на {value} в таблице откликов. {ex}')


def update_field_by_response_id(response_id, field, value):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''UPDATE responses
                        SET {field}=?
                        WHERE id=?
                        ''', (value, response_id,))

        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Поле ({field}) в отклике {response_id} изменено на {value} в таблице заявок.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось изменить поле ({field}) в отклике {response_id} на {value} в таблице заявок. {ex}')


#TODO Удаление данных
def delete_response(user_id):
    try:
        database = sqlite3.connect("db.db")
        cursor = database.cursor()

        cursor.execute(f'''
            DELETE FROM responses
            WHERE seller=? AND (status=? OR status=?)
            ''', (user_id, 'created', 'creating',))
            
        database.commit()
        cursor.close()
        database.close()

        logging.info(f'{inspect.currentframe().f_code.co_name}: Отклик пользователя {user_id} удален.')

    except Exception as ex:
        logging.error(f'{inspect.currentframe().f_code.co_name}: Ошибка при удалении отклика пользователя ({user_id}). {ex}')


#! ИЗВЛЕЧЕНИЕ ВСЕХ ДАННЫХ
def select_db_users():
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users_info = cursor.execute('SELECT * FROM users').fetchall()
    
    cursor.close()
    database.close()

    return users_info


def select_db_orders():
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users_info = cursor.execute('SELECT * FROM orders').fetchall()
    
    cursor.close()
    database.close()

    return users_info


def select_db_responses():
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users_info = cursor.execute('SELECT * FROM responses').fetchall()
    
    cursor.close()
    database.close()

    return users_info


#! ДЛЯ ТЕСТИРОВАНИЯ
def delete_user(user_id):
    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'DELETE FROM users WHERE user_id=?', (user_id,))

    database.commit()
    cursor.close()
    database.close()