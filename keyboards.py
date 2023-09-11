import math

from telebot import types

import config
import db_functions


def role_keyboard():

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    keyboard.add(types.KeyboardButton('Покупатель'), types.KeyboardButton('Продавец'))

    return keyboard


def confirm_data_keyboard(data):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_{data}'))

    return keyboard


def request_phone_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    keyboard.add(types.KeyboardButton(text = 'Предоставить номер', request_contact=True,))

    return keyboard


def request_country_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    keyboard.add(types.KeyboardButton(text = 'Отправить геолокацию', request_location=True,))

    return keyboard


def countries_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    countries = []

    for num, country in enumerate(config.COUNTRIES):
        countries.append(types.InlineKeyboardButton(country, callback_data = f'country_{country}'))

        if num % 2 != 0 or num == len(config.COUNTRIES) - 1:
            keyboard.add(*countries)
            countries = []

    return keyboard


def change_profile_keyboard(role, check_in = True):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('👥 Изменить имя', callback_data = f'change_profile_name'))
    keyboard.add(types.InlineKeyboardButton('📇 Изменить фамилию', callback_data = f'change_profile_family-name'))
    keyboard.add(types.InlineKeyboardButton('🎭 Изменить роль', callback_data = f'change_profile_role'))
    keyboard.add(types.InlineKeyboardButton('📱 Изменить номер', callback_data = f'change_profile_phone'))
    keyboard.add(types.InlineKeyboardButton('📧 Изменить e-mail', callback_data = f'change_profile_email'))
    keyboard.add(types.InlineKeyboardButton('🌎 Изменить страну', callback_data = f'change_profile_country'))

    if role == 'seller':
        keyboard.add(types.InlineKeyboardButton('🎛 Настройки приема заказов', callback_data = f'change_profile_settings'))

    if check_in:
        keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_profile'))
    else:
        keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))
    
    return keyboard


def change_order_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('🏠 Изменить адрес', callback_data = f'change_order_address'))
    keyboard.add(types.InlineKeyboardButton('📁 Изменить наименование', callback_data = f'change_order_name'))
    keyboard.add(types.InlineKeyboardButton('📷 Изменить фотографию', callback_data = f'change_order_photo'))
    keyboard.add(types.InlineKeyboardButton('📝 Изменить комментарий', callback_data = f'change_order_comment'))
    keyboard.add(types.InlineKeyboardButton('🌎 Изменить страну', callback_data = f'change_order_country'))
    keyboard.add(types.InlineKeyboardButton('🔗 Изменить ссылку', callback_data = f'change_order_link'))
    
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_order'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel_order'))

    return keyboard


def change_response_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('💵 Изменить цену', callback_data = f'change_response_price'))
    keyboard.add(types.InlineKeyboardButton('📦 Настройки доставки', callback_data = f'change_response_delivery'))
    keyboard.add(types.InlineKeyboardButton('📝 Изменить комментарий', callback_data = f'change_response_comment'))
    
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_response'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel_response'))

    return keyboard


def main_keyboard(role):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if role == 'seller':
        keyboard.add(types.KeyboardButton('🗂 Профиль'), types.KeyboardButton('💵 Мои отклики'))
        keyboard.add(types.KeyboardButton('🛒 Мои заявки'))
    else:
        keyboard.add(types.KeyboardButton('🗂 Профиль'), types.KeyboardButton('🛒 Мои заявки'))

    keyboard.add(types.KeyboardButton('❓ Помощь/справка'))

    return keyboard


def orders_keyboard(orders, page, status_filter):
    keyboard = types.InlineKeyboardMarkup(row_width=5)

    pages = math.ceil(len(orders) / config.ON_PAGE)

    filtered_orders = []
    for order in orders:
        status = order[2]

        if status == 'checking':
            status = '👨‍💼'
        elif status == 'declined':
            status = '⛔️'
        elif status == 'searching':
            status = '🔍'
        elif status == 'waiting_payment':
            status = '💵'
        elif status == 'waiting_confirm': 
            status = '💳'
        elif status == 'waiting_buy':
            status = '🛍'
        elif status == 'waiting_departure':
            status = '📦'
        elif status == 'waiting_delivery':
            status = '⏳'
        elif status == 'done':
            status = '✅'
        elif status == 'canceled':
            status = '❌'

        if (status_filter == 'all' or status_filter == status) and status != 'creating' and status != 'created':
            filtered_orders.append(order)
    
    for num, order in enumerate(filtered_orders[config.ON_PAGE*page-config.ON_PAGE:config.ON_PAGE*page]):
        order_id = order[0]
        name = order[1]
        status = order[2]

        if status == 'checking':
            status = '👨‍💼'
        elif status == 'declined':
            status = '⛔️'
        elif status == 'searching':
            status = '🔍'
        elif status == 'waiting_payment':
            status = '💵'
        elif status == 'waiting_confirm': 
            status = '💳'
        elif status == 'waiting_buy':
            status = '🛍'
        elif status == 'waiting_departure':
            status = '📦'
        elif status == 'waiting_delivery':
            status = '⏳'
        elif status == 'done':
            status = '✅'
        elif status == 'canceled':
            status = '❌'
        
        keyboard.add(types.InlineKeyboardButton(f'{status} - {num + 1 + config.ON_PAGE * (page - 1)}. {name.capitalize()} ({order_id})', callback_data = f'order_{order_id}_{page}'))


    begin_callback = f'page_order_1'
    back_callback = f'page_order_{page - 1}'
    forward_callback = f'page_order_{page + 1}'
    end_callback = f'page_order_{pages}'

    if page == 1:
        begin_callback = 'not_available'
        back_callback = 'not_available'
    elif page == pages:
        forward_callback = 'not_available'
        end_callback = 'not_available'
    
    if len(filtered_orders) > config.ON_PAGE:
        begin = types.InlineKeyboardButton('<<<', callback_data = begin_callback)
        back = types.InlineKeyboardButton('<-', callback_data = back_callback)
        page = types.InlineKeyboardButton(f'{page}/{pages}', callback_data = 'not_available')
        forward = types.InlineKeyboardButton('->', callback_data = forward_callback)
        end = types.InlineKeyboardButton('>>>', callback_data = end_callback)
        keyboard.add(begin, back, page, forward, end)

    if orders:
        buttons = []
        for num, default_status in enumerate(config.ORDER_STATUSES):
            symbol = ''

            if status_filter == default_status:
                symbol = '📌 - '
            
            buttons.append(types.InlineKeyboardButton(f'{symbol}{default_status}', callback_data = f'filter_orders_{default_status}'))

            if (num + 1) % 3 == 0 or num == len(config.ORDER_STATUSES) - 1:
                keyboard.add(*buttons)
                buttons = []

    keyboard.add(types.InlineKeyboardButton('🆕 Новый заказ', callback_data = f'new_order'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def responses_keyboard(responses, page, status_filter):
    keyboard = types.InlineKeyboardMarkup(row_width=5)

    pages = math.ceil(len(responses) / config.ON_PAGE)

    filtered_responses = []
    for response in responses:
        status = response[2]

        if status == 'sended':
            status = '🔍'
        elif status == 'declined':
            status = '⛔️'
        elif status == 'canceled':
            status = '❌'
        elif status == 'waiting_payment':
            status = '💵'
        elif status == 'waiting_confirm': 
            status = '💳'
        elif status == 'waiting_buy':
            status = '🛍'
        elif status == 'waiting_departure':
            status = '📦'
        elif status == 'waiting_delivery':
            status = '⏳'
        elif status == 'waiting_transfer':
            status = '💰'
        elif status == 'done':
            status = '✅'

        if (status_filter == 'all' or status_filter == status) and status != 'creating' and status != 'created':
            filtered_responses.append(response)
    
    for num, response in enumerate(filtered_responses[config.ON_PAGE*page-config.ON_PAGE:config.ON_PAGE*page]):
        response_id = response[0]
        name = response[1]
        status = response[2]
        order_id = response[3]

        if status == 'sended':
            status = '🔍'
        elif status == 'declined':
            status = '⛔️'
        elif status == 'canceled':
            status = '❌'
        elif status == 'waiting_payment':
            status = '💵'
        elif status == 'waiting_confirm': 
            status = '💳'
        elif status == 'waiting_buy':
            status = '🛍'
        elif status == 'waiting_departure':
            status = '📦'
        elif status == 'waiting_delivery':
            status = '⏳'
        elif status == 'waiting_transfer':
            status = '💰'
        elif status == 'done':
            status = '✅'
        
        keyboard.add(types.InlineKeyboardButton(f'{status} - {num + 1 + config.ON_PAGE * (page - 1)}. {name.capitalize()} ({order_id})', callback_data = f'respond_{response_id}_{page}'))


    begin_callback = f'page_response_1'
    back_callback = f'page_response_{page - 1}'
    forward_callback = f'page_response_{page + 1}'
    end_callback = f'page_response_{pages}'

    if page == 1:
        begin_callback = 'not_available'
        back_callback = 'not_available'
    elif page == pages:
        forward_callback = 'not_available'
        end_callback = 'not_available'
    
    if len(filtered_responses) > config.ON_PAGE:
        begin = types.InlineKeyboardButton('<<<', callback_data = begin_callback)
        back = types.InlineKeyboardButton('<-', callback_data = back_callback)
        page = types.InlineKeyboardButton(f'{page}/{pages}', callback_data = 'not_available')
        forward = types.InlineKeyboardButton('->', callback_data = forward_callback)
        end = types.InlineKeyboardButton('>>>', callback_data = end_callback)
        keyboard.add(begin, back, page, forward, end)

    if responses:
        buttons = []
        for num, default_status in enumerate(config.RESPONSE_STATUSES):
            symbol = ''

            if status_filter == default_status:
                symbol = '📌 - '
            
            buttons.append(types.InlineKeyboardButton(f'{symbol}{default_status}', callback_data = f'filter_responses_{default_status}'))

            if (num + 1) % 3 == 0 or num == len(config.ORDER_STATUSES) - 1:
                keyboard.add(*buttons)
                buttons = []

    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def addresses_keyboard(addresses):
    keyboard = types.InlineKeyboardMarkup()

    for index, address in enumerate(addresses):
        keyboard.add(types.InlineKeyboardButton(address, callback_data = f'address_{index}'))

    return keyboard


def confirm_address_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    correct = types.InlineKeyboardButton('Верный адрес', callback_data = f'confirm_address')
    reenter = types.InlineKeyboardButton('Ввести заново', callback_data = f'decline_address')

    keyboard.add(correct, reenter)

    return keyboard


def order_keyboard(page, status, order_id):
    keyboard = types.InlineKeyboardMarkup()

    if status == 'waiting_payment':
        keyboard.add(types.InlineKeyboardButton('💵 Оплатить', callback_data = f'pay_{order_id}'))
    elif status == 'waiting_delivery':
        keyboard.add(types.InlineKeyboardButton('✅ Товар получен', callback_data = f'received_{order_id}'))

    if status in config.ORDERS_STATUSES_WITH_RESPONSE:
        response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
        keyboard.add(types.InlineKeyboardButton('🔍 Посмотреть отклик', callback_data = f'view_response_{response_id}_others'))

    if status == 'searching' or status == 'waiting_payment' or status == 'checking':
        keyboard.add(types.InlineKeyboardButton('🗑 Отменить', callback_data = f'revoke_order_{order_id}'))
    
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_orders_{page}'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def response_keyboard(page, status, response_id, order_id):
    keyboard = types.InlineKeyboardMarkup()

    if status == 'sended':
        keyboard.add(types.InlineKeyboardButton('🗑 Отменить', callback_data = f'revoke_response_{response_id}_{page}'))
    elif status == 'waiting_buy':
        keyboard.add(types.InlineKeyboardButton('🛍 Товар куплен', callback_data = f'bought_{response_id}_{order_id}_{page}'))
    elif status == 'waiting_departure':
        keyboard.add(types.InlineKeyboardButton('📦 Товар отправлен', callback_data = f'sended_{response_id}_{order_id}_{page}'))

    keyboard.add(types.InlineKeyboardButton('🔍 Посмотреть заявку', callback_data = f'view_order_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_responses_{page}'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def manager_keyboard():
    keyboard = types.InlineKeyboardMarkup() 
    
    keyboard.add(types.InlineKeyboardButton('💬 Чат с менеджером', url = f'https://t.me/{config.MANAGER_USERNAME}'))
    keyboard.add(types.InlineKeyboardButton('🛠 Инструкция', url = config.INSTRUCTION))
    keyboard.add(types.InlineKeyboardButton('🔒 Почему с нами безопасно?', url = config.SAFETY))
    keyboard.add(types.InlineKeyboardButton('✨ Рекомендации по использованию', url = config.ADVISE))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def settings_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    
    keyboard.add(types.InlineKeyboardButton('🌏 Весь мир', callback_data = f'settings_whole'))
    keyboard.add(types.InlineKeyboardButton('📍 Страна пребывания', callback_data = f'settings_country'))

    return keyboard


def order_inspect_keyboard(order_id, buyer_id):
    keyboard = types.InlineKeyboardMarkup()
    
    keyboard.add(types.InlineKeyboardButton('✅ Принять', callback_data = f'inspect_confirm_{order_id}_{buyer_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data = f'inspect_reject_{order_id}_{buyer_id}'))

    return keyboard


def response_order_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('🙋‍♂️ Откликнуться', callback_data = f'response_confirm_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('⏭ Пропустить', callback_data = f'response_skip_{order_id}'))

    return keyboard


def confirm_skip_order_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('⏭ Пропустить', callback_data = f'skip_confirm_{order_id}'), types.InlineKeyboardButton('⬅️ Назад', callback_data = f'skip_cancel_{order_id}'))

    return keyboard


def delivery_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('📦 С доставкой', callback_data = f'delivery_include'), types.InlineKeyboardButton('🙅‍♂️ Без доставки', callback_data = f'delivery_no'))

    return keyboard


def confirm_cancel_response_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('❌ Отменить отклик', callback_data = f'delete_confirm'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'delete_cancel'))

    return keyboard


def get_response_keyboard(response_id, order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Принять', callback_data = f'deal_accept_{response_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data = f'deal_decline_{response_id}'))
    keyboard.add(types.InlineKeyboardButton('🔍 Посмотреть заявку', callback_data = f'view_order_{order_id}'))

    return keyboard


def confirm_account_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'account_confirm'))
    keyboard.add(types.InlineKeyboardButton('🔄 Ввести заново', callback_data = f'account_reenter'))

    return keyboard


def payment_method_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('СБП (по номеру телефона)', callback_data = 'method_sbp'))
    keyboard.add(types.InlineKeyboardButton('По номеру карты', callback_data = 'method_card'))

    return keyboard


def banks_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    sber = types.InlineKeyboardButton('Сбер', callback_data = 'bank_sber')
    tinkoff = types.InlineKeyboardButton('Тинькофф', callback_data = 'bank_tinkoff')
    vtb = types.InlineKeyboardButton('ВТБ', callback_data = 'bank_vtb')
    open = types.InlineKeyboardButton('Открытие', callback_data = 'bank_open')
    
    keyboard.add(sber, tinkoff)
    keyboard.add(vtb, open)

    keyboard.add(types.InlineKeyboardButton('Альфа-Банк', callback_data = 'bank_alfa'))
    keyboard.add(types.InlineKeyboardButton('Райффайзен Банк', callback_data = 'bank_raif'))

    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = 'back_method_1'))
    
    return keyboard


def confirm_accept_keyboard(response_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Принять', callback_data = f'accept_confirm_{response_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'accept_cancel_{response_id}'))

    return keyboard


def confirm_decline_keyboard(response_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('❌ Отклонить отклик', callback_data = f'annul_confirm_{response_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'annul_cancel_{response_id}'))

    return keyboard


def view_order_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('🔍 Посмотреть заявку', callback_data = f'view_order_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def confirm_revoke_response_keyboard(response_id, page):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('❌ Отозвать отклик', callback_data = f'void_confirm_{response_id}_{page}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'void_cancel_{response_id}_{page}'))

    return keyboard


def order_paid(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Оплачено', callback_data = f'paid_order_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def payment_photo_confirmation_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Отправить', callback_data = f'payment-photo_confirm_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('🔄 Ввести заново', callback_data = f'payment-photo_reenter_{order_id}'))

    return keyboard

def payment_inspect_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'payment-inspect_confirm_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Отклонить', callback_data = f'payment-inspect_cancel_{order_id}'))

    return keyboard


def view_order_response_keyboard(order_id, response_id, instance = 'my'):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('🔍 Посмотреть заявку', callback_data = f'view_order_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('👓 Посмотреть отклик', callback_data = f'view_response_{response_id}_{instance}'))
    keyboard.add(types.InlineKeyboardButton('❌ Закрыть', callback_data = f'close'))

    return keyboard


def received_confirm_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirmation_received_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'close'))

    return keyboard


def bought_confirm_keyboard(order_id, response_id, page):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirmation_bought_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_response_{page}_{response_id}'))

    return keyboard


def sended_confirm_keyboard(order_id, response_id, page):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirmation_sended_{order_id}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data = f'back_response_{page}_{response_id}'))

    return keyboard


def transfer_keyboard(order_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton('✅ Перевод совершен', callback_data = f'transfer_{order_id}'))

    return keyboard