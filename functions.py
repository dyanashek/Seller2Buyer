import telebot
import logging
import inspect

import keyboards
import text
import db_functions
import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def order_to_inspect_by_admins(order_id):
    order_info = db_functions.get_all_order_info_by_order_id(order_id)

    buyer = order_info[1]
    username = db_functions.get_field_info(buyer, 'username')
    address = order_info[6]
    name = order_info[7]
    photo = order_info[8]
    comment = order_info[9]
    country = order_info[10]
    link = order_info[11]

    reply_text = text.inspect_order(order_id, address, name, comment, country, link, username)

    for user_id in config.MANAGER_ID:

        try:
            bot.send_photo(chat_id=user_id,
                           photo=photo,
                           caption=reply_text,
                           reply_markup=keyboards.order_inspect_keyboard(order_id, buyer),
                           parse_mode='Markdown',
                           )

        except Exception as ex:
            logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить заявку ({order_id}) на согласование администратору {user_id}. {ex}')


def notify_sellers_new_order(order_id, buyer_id):
    order_info = db_functions.get_all_order_info_by_order_id(order_id)

    address = order_info[6]
    name = order_info[7]
    photo = order_info[8]
    comment = order_info[9]
    country = order_info[10]
    link = order_info[11]

    reply_text = text.notify_sellers_new_order(order_id, address, name, comment, country, link)
    users_ids = db_functions.get_interested_sellers(buyer_id, country)

    for user_id in users_ids:
        try:
            bot.send_photo(chat_id=user_id,
                           photo=photo,
                           caption=reply_text,
                           reply_markup=keyboards.response_order_keyboard(order_id),
                           parse_mode='Markdown',
                           )

            notified = eval(db_functions.get_field_info_by_order_id(order_id, 'notified'))
            notified.append(str(user_id))
            db_functions.update_field_by_order_id(order_id, 'notified', str(notified))

        except Exception as ex:
            logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить заявку ({order_id}) продавцу {user_id}. {ex}')


def notify_seller_unfinished_orders(user_id, orders_ids):
    for order_id in orders_ids:
        order_info = db_functions.get_all_order_info_by_order_id(order_id)

        address = order_info[6]
        name = order_info[7]
        photo = order_info[8]
        comment = order_info[9]
        country = order_info[10]
        link = order_info[11]

        reply_text = text.notify_sellers_new_order(order_id, address, name, comment, country, link)

        try:
            bot.send_photo(chat_id=user_id,
                           photo=photo,
                           caption=reply_text,
                           reply_markup=keyboards.response_order_keyboard(order_id),
                           parse_mode='Markdown',
                           )

            notified = eval(db_functions.get_field_info_by_order_id(order_id, 'notified'))
            notified.append(str(user_id))
            db_functions.update_field_by_order_id(order_id, 'notified', str(notified))

        except Exception as ex:
            logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить заявку ({order_id}) продавцу {user_id}. {ex}')


def payment_to_inspect_by_admins(order_id, response_id):
    for user_id in config.MANAGER_ID:
        price = db_functions.get_field_info_by_response_id(response_id, 'price')
        photo = db_functions.get_field_info_by_order_id(order_id, 'payment_photo')

        try:
            bot.send_photo(chat_id=user_id,
                           photo=photo,
                           caption=text.verify_payment(price, order_id),
                           reply_markup=keyboards.payment_inspect_keyboard(order_id),
                           parse_mode='Markdown',
                           )

        except Exception as ex:
            logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить подтверждение оплаты ({order_id}) на согласование администратору {user_id}. {ex}')


def to_transfer_by_admins(order_id, response_id):
    payment_form = db_functions.get_field_info_by_response_id(response_id, 'payment_form')
    bank = db_functions.get_field_info_by_response_id(response_id, 'bank')
    account = db_functions.get_field_info_by_response_id(response_id, 'account')

    name = db_functions.get_field_info_by_order_id(order_id, 'name')
    price = db_functions.get_field_info_by_response_id(response_id, 'price')

    for user_id in config.MANAGER_ID:
        try:
            bot.send_message(chat_id=user_id,
                             text=text.transfer(order_id, name, payment_form, bank, account, price),
                             reply_markup=keyboards.transfer_keyboard(order_id),
                             parse_mode='Markdown',
                             )

        except Exception as ex:
            logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить реквизиты для платежа по отклику({response_id}) администратору {user_id}. {ex}')


def data_to_google(user_id):
    users_info = db_functions.select_db_users()
    work_sheet = config.TABLE.worksheet(config.USERS_LIST_NAME)
    work_sheet.update(f'A2:U{len(users_info) + 1}', users_info)

    orders_info = db_functions.select_db_orders()
    work_sheet = config.TABLE.worksheet(config.ORDERS_LIST_NAME)
    work_sheet.update(f'A2:P{len(orders_info) + 1}', orders_info)

    responses_info = db_functions.select_db_responses()
    work_sheet = config.TABLE.worksheet(config.RESPONSES_LIST_NAME)
    work_sheet.update(f'A2:L{len(responses_info) + 1}', responses_info)

    try:
        bot.send_message(chat_id=user_id,
                         text=text.DATA_TRANSFERRED,
                         )
    except:
        pass


def send_log(user_id):
    with open(f'py_log.log', "rb") as f:
        file_data = f.read()

    bot.send_document(chat_id=user_id,
                    document=file_data,
                    visible_file_name=f'py_log.log', 
                    )