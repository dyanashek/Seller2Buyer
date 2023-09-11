import config
import utils


#! ИНФОРМАЦИОННЫЕ СООБЩЕНИЯ
WELCOME_MESSAGE = '''
                \nПривет!\
                \nНаш сервис позволяет....\
                \nДля начала использования необходимо *зарегистрироваться*, этот процесс займет меньше минуты!\
                \n\
                \nВыбери роль, в которой будешь выступать на нашей площадке: *(ее всегда можно изменить позже)*\
                \n*Покупатель* - ищешь где заказать редкий товар, хочешь найти байера, который его отправит!\
                \n*Продавец* - ищешь способ заработать и имеешь выход на сложнодоступные рынки (ты так же сможешь заказывать интересные тебе товары в роли покупателя).\
                '''

OUTDATED_MESSAGE = 'Данные устарели.'

PROFILE_CONFIRM = 'Данные профиля *успешно сохранены*.'

CANCEL_COMMAND = '\n\nДля отмены изменений воспользуйтесь командой */cancel*.'

HELP = 'Выбери *интересующий раздел* или перейди в чат с *менеджером*:'

INPUT_CANCELED = 'Ввод *успешно отменен*.'

STATUS_UPDATED = 'Статус *обновлен*.'

#! ОШИБКИ ВВОДА
ROLE_WRONG_INPUT = '''
                \nПожалуйста, выбери роль, в которой будешь выступать на нашей площадке: *(ее всегда можно изменить позже)*\
                \n\
                \n*Покупатель* - ищешь где заказать редкий товар, хочешь найти байера, который его отправит!\
                \n*Продавец* - ищешь способ заработать и имеешь выход на сложнодоступные рынки (ты так же сможешь заказывать интересные тебе товары в роли покупателя).\
                '''

WRONG_COUNTRY_METHOD = '''
                        \nВыбрана роль *продавца*, нам необходимо валидировать твое местоположение, чтобы отправлять заявки от покупателей.\
                        \nВоспользуйся кнопкой "отправить геолокацию".\
                        '''

NO_INPUT = 'Не ожидается информации для ввода.'


#! ОШИБКИ ЗАПРОСА
LOCATION_ERROR = 'К сожалению, *не удалось* определить твое местоположение, попробуй *отправить геолокацию позже* или когда будешь *в другом месте*.'

LOCATION_NEEDED = 'Для завершения регистрации необходимо указать страну прибывания.'

CANT_CHANGE_ROLE = 'Невозможно изменить роль, у тебя есть отклики, не достигшие *конечного статуса*. Отмени их или выполни обязательства.\n\nВоспользуйся кнопкой *помощь* в нестандартной ситуации.'

CANT_CONFIRM_OUTDATED_DATA = 'Невозможно изменить статус, *данные устарели*, обнови данные через *меню*.'

#! ОШИБКИ РОЛИ
RESPONSE_ORDER_ROLE_ERROR = 'На заявки могут откликаться только пользователи с ролью *продавец*.'

#! ЗАПРОСЫ ВВОДА
WHOLE_WORLD = 'Выбери настройки для приема заказов:\n\n*Весь мир* - заявки будут приходить для всех товаров;\n*Страна пребывания* - будут приходить заявки по товарам, которые по мнению заказчиках можно найти в стране вашего пребывания, либо если заказчик не знает где можно найти интересующий его товар.'

ASK_NAME = 'Пожалуйста, укажи свое *имя*.'

ASK_FAMILY_NAME = 'Пожалуйста, укажи свою *фамилию*.'

ASK_PHONE = 'Пожалуйста, укажи свой *номер* или воспользуйся кнопкой *"предоставить номер"*, если он совпадает с аккаунтом telegram.'

ASK_EMAIL = 'Пожалуйста, укажи свой *e-mail адрес*.'

ASK_COUNTRY_BUYER = 'Выбери из списка *страну*, в которой находишься или введи ее название в чат.'

ASK_COUNTRY_SELLER = '*Продавцам* необходимо предоставить информацию о стране, в которой они находятся. Для этого воспользуйся кнопкой "Отправить геолокацию".'


#! ЗАЯВКИ ПОКУПАТЕЛЕЙ
CANCEL_ORDER_COMMAND = '\n\nВоспользуйся командой */cancel_order* если передумал и хочешь отменить заявку.'

INPUT_ADDRESS = 'Введи *адрес* для доставки, указав *страну и город*.' + CANCEL_ORDER_COMMAND

INPUT_OR_CHOOSE_ADDRESS = 'Введи *адрес* для доставки, указав *страну и город* или выбери один из списка ниже.' + CANCEL_ORDER_COMMAND

PRODUCT_NAME = 'Укажи *наименование товара (бренд, модель, артикул)*.\nЕсли представленных данных будет недостаточно для идентификации модели - заявка может быть отклонена администраторами.' + CANCEL_ORDER_COMMAND

PRODUCT_PHOTO = 'Отправь *фотографию товара*, товар должен быть хорошо различимым, желательно на белом фоне.' + CANCEL_ORDER_COMMAND

PRODUCT_COMMENT = 'Укажи *комментарии к заказу*, воспользуйся командой */skip* для пропуска этого шага.' + CANCEL_ORDER_COMMAND

PRODUCT_COUNTRY = 'Укажи *страну*, в которой можно найти интересующий товар. Воспользуйся командой */skip* для пропуска этого шага.' + CANCEL_ORDER_COMMAND

PRODUCT_LINK = 'Укажи *ссылку на товар*. Воспользуйся командой */skip* для пропуска этого шага.' + CANCEL_ORDER_COMMAND

SEND_TO_ADMIN = 'Твоя заявка отправлена на рассмотрение администраторам. Мы пришлем уведомление об изменении ее статуса, который также можно посмотреть в разделе *мои заявки*.'

ORDER_CANCELED = 'Заявка *успешно* отменена.\nУправление заявками осуществляется в разделе *мои заявки*.'

#! ОШИБКИ ПРИ СОЗДАНИИ ЗАКАЗА
UNFINISHED_ORDER = 'У тебя есть неподтвержденная заявка, прежде чем создавать новую воспользуйся командой */cancel_order* или подтверди предыдущую.'

NO_MEDIA_GROUP = 'Пожалуйста, отправля *по одной фотографии* за раз.'


#! f-строки
def confirm_name(name):
    name = utils.escape_markdown(name)

    reply = f'''
            \nТвое имя *{name}*?\
            \nНажми "подтвердить" или отправь верное имя в чат.\
            '''

    return reply


def confirm_family_name(family_name):
    family_name = utils.escape_markdown(family_name)

    reply = f'''
            \nТвоя фамилия *{family_name}*?\
            \nНажми "подтвердить" или отправь верную фамилию в чат.\
            '''

    return reply


def confirm_profile(role, name, family_name, phone, email, country, whole_world):
    name = utils.escape_markdown(name)
    family_name = utils.escape_markdown(family_name)
    phone = utils.escape_markdown(phone)
    email = utils.escape_markdown(email)
    country = utils.escape_markdown(country)

    reply = f'''
            \n*{config.ROLES_ENG[role]}*\
            \n\
            \n*Имя:* {name}\
            \n*Фамилия:* {family_name}\
            \n*Номер телефона:* {phone}\
            \n*E-mail:* {email}\
            \n*Страна:* {country.capitalize()}\
            '''
    if role == 'seller':
        if whole_world:
            settings = '\n*Настройки приема заявок:* весь мир'
        else:
            settings = '\n*Настройки приема заявок:* страна пребывания'
        
        reply += settings

    return reply


def found_location(country):
    country = utils.escape_markdown(country)

    return f'Местоположение определено: *{country.capitalize()}*.'


def confirm_address(address):
    address = utils.escape_markdown(address)

    return f'Проверь адрес:\n*{address}*'


def confirm_order(address, name, photo, comment, country, link):
    address = utils.escape_markdown(address)
    name = utils.escape_markdown(name)
    comment = utils.escape_markdown(comment)
    country = utils.escape_markdown(country)
    link = utils.escape_markdown(link)

    reply_text = f'''
                \nПроверь информацию и воспользуйся кнопкой *подтвердить*\
                \n\
                \n*Твой заказ:*\
                \n\
                \n*Адрес:* {address}\
                \n*Наименование:* {name}\
                \n*Комментарий:* {comment}\
                \n*Где найти:* {country.capitalize()}\
                \n*Ссылка:* {link}\
                '''
    
    return reply_text


def order_info(order_id, status, reason, address, name, photo, comment, country, link):
    if reason:
        reason = utils.escape_markdown(reason)
    address = utils.escape_markdown(address)
    name = utils.escape_markdown(name)
    comment = utils.escape_markdown(comment)
    country = utils.escape_markdown(country)
    link = utils.escape_markdown(link)

    status_text = config.ORDERS_STATUSES_LEGEND[status]
    if status == 'declined':
        status_text += f' ({reason})'
    
    reply_text = f'''
                \n*{status_text}*\
                \n\
                \n*Адрес:* {address}\
                \n*Наименование:* {name} ({order_id})\
                \n*Комментарий:* {comment}\
                \n*Где найти:* {country}\
                \n*Ссылка:* {link}\
                '''
    
    return reply_text


def orders_legend(status_filter):
    if status_filter == 'all':
        status_filter = '🙌🏻 - все заявки'

    reply_text = f'''
                \n*МОИ ЗАЯВКИ*\
                \n*Активирован фильтр:* {status_filter}\
                \n\
                \n👨‍💼 - заявка на одобрении у менеджера\
                \n⛔️ - не одобрена менеджером\
                \n🔍 - поиск исполнителя\
                \n💵 - ожидается оплата заказчиком\
                \n💳 - ожидается верификация платежа\
                \n🛍 - ожидается подтверждение покупки\
                \n📦 - ожидается подтверждение отправки\
                \n⏳ - ожидается доставка\
                \n✅ - товар получен\
                \n❌ - заявка отменена\
                '''
    
    return reply_text


def responses_legend(status_filter):
    if status_filter == 'all':
        status_filter = '🙌🏻 - все заявки'

    reply_text = f'''
                \n*МОИ ОТКЛИКИ*\
                \n*Активирован фильтр:* {status_filter}\
                \n\
                \n🔍 - отклик отправлен покупателю\
                \n⛔️ - отклонен покупателем\
                \n❌ - отменен продавцом\
                \n💵 - ожидается оплата заказчиком\
                \n💳 - ожидается верификация платежа\
                \n🛍 - ожидается подтверждение покупки\
                \n📦 - ожидается подтверждение отправки\
                \n⏳ - ожидается доставка\
                \n💰 - ожидается получение вознаграждения\
                \n✅ - получена оплата\
                '''
    
    return reply_text


def inspect_order(order_id, address, name, comment, country, link, username):
    address = utils.escape_markdown(address)
    name = utils.escape_markdown(name)
    comment = utils.escape_markdown(comment)
    country = utils.escape_markdown(country)
    link = utils.escape_markdown(link)
    username = utils.escape_markdown(username)

    reply_text = f'''
                \nПользователь @{username} хочет разместить следующий заказ:\
                \n\
                \n*Адрес:* {address}\
                \n*Наименование:* {name}\
                \n*Комментарий:* {comment}\
                \n*Где найти:* {country.capitalize()}\
                \n*Ссылка:* {link}\
                '''
    
    return reply_text


def order_inspected_confirm(order_id, name):
    name = utils.escape_markdown(name)

    return f'Твоя заявка *{name} ({order_id})* одобрена администратором.\nУправление заявками осуществляется в разделе *мои заявки*.'


def order_inspected_reject(order_id, name, reason):
    name = utils.escape_markdown(name)
    reason = utils.escape_markdown(reason)

    return f'Твоя заявка *{name} ({order_id})* отклонена администратором.\n*Причина:* {reason}\n\nУправление заявками осуществляется в разделе *мои заявки*.'


def notify_sellers_new_order(order_id, address, name, comment, country, link):
    address = utils.escape_markdown(address)
    name = utils.escape_markdown(name)
    comment = utils.escape_markdown(comment)
    country = utils.escape_markdown(country)
    link = utils.escape_markdown(link)

    reply_text = f'''
                \nРазмещен следующий заказ:\
                \n\
                \n*Адрес:* {address}\
                \n*Наименование:* {name} ({order_id})\
                \n*Комментарий:* {comment}\
                \n*Где найти:* {country.capitalize()}\
                \n*Ссылка:* {link}\
                '''
    
    return reply_text


def ask_response_price(name):
    name = utils.escape_markdown(name)

    return f'Укажи *цену в рублях*, по которой готов отправить заказанный товар ({name}).\nПринимай во внимание возможные колебания валютного курса.' + CANCEL_RESPONSE_COMMAND


def incorrect_price(name):
    name = utils.escape_markdown(name)

    return f'Цена не соответствует формату.\nУкажи *цену в рублях*, по которой готов отправить заказанный товар ({name}).' + CANCEL_RESPONSE_COMMAND


def ask_delivery(name, price):
    name = utils.escape_markdown(name)
    price = utils.numbers_format(price)

    return f'Цена *({price} руб.)* за {name} указана с учетом доставки или без?' + CANCEL_RESPONSE_COMMAND


def confirm_response(order_id, name, price, delivery, comment):
    name = utils.escape_markdown(name)
    price = utils.numbers_format(price)
    if delivery:
        delivery = 'включена в стоимость'
    else:
        delivery = 'не включена в стоимость'
    
    comment = utils.escape_markdown(comment)

    reply_text = f'''
                \nПроверь *свой отклик* на заявку: {name} ({order_id})\
                \nНажми "подтвердить", если все заполнено верно.\
                \n\
                \n*Цена:* {price} руб.\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                '''
    
    return reply_text


def get_response(username, order_id, name, price, delivery, comment):
    username = utils.escape_markdown(username)
    name = utils.escape_markdown(name)
    price_text = utils.numbers_format(price * (1 + config.PERCENT))
    percent = utils.numbers_format(price * config.PERCENT)

    if delivery:
        delivery = 'включена в стоимость'
    else:
        delivery = 'не включена в стоимость'
    
    comment = utils.escape_markdown(comment)

    reply_text = f'''
                \nОтклик на заявку {name} ({order_id}) от пользователя @{username}:\
                \n\
                \n*Цена:* {price_text} руб. (в т.ч. {percent} руб. - комиссия сервиса)\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                '''
    
    return reply_text


def response_info(status, name, price, delivery, comment, order_id):
    name = utils.escape_markdown(name)
    price = utils.numbers_format(price)

    if delivery:
        delivery = 'включена в стоимость'
    else:
        delivery = 'не включена в стоимость'
    
    comment = utils.escape_markdown(comment)

    status_text = config.RESPONSES_STATUSES_LEGEND[status]

    reply_text = f'''
                \nОтклик на заявку {name} ({order_id}):\
                \n\
                \n*{status_text}*\
                \n\
                \n*Цена:* {price} руб.\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                '''
    
    return reply_text


def others_response_info(seller_username, status, name, price, delivery, comment, order_id):
    name = utils.escape_markdown(name)
    price_text = utils.numbers_format(price * (1 + config.PERCENT))
    percent = utils.numbers_format(price * config.PERCENT)

    if delivery:
        delivery = 'включена в стоимость'
    else:
        delivery = 'не включена в стоимость'
    
    comment = utils.escape_markdown(comment)
    seller_username = utils.escape_markdown(seller_username)

    reply_text = f'''
                \nОтклик на заявку {name} ({order_id}) от пользователя @{seller_username}:\
                \n\
                \n*Цена:* {price_text} руб. (в т.ч. {percent} руб. - комиссия сервиса)\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                '''
    
    return reply_text


def confirm_bank_account(payment_form, bank, account):
    if payment_form == 'sbp':
        payment_form = 'СБП (по номеру телефона)'
        method = 'Номер телефона'
    elif payment_form == 'card':
        payment_form = 'По номеру карты'
        method = 'Номер карты'

    bank = config.BANKS[bank]

    reply_text = f'''
                \nПодтверди реквизиты для получения выплаты\
                \n*{payment_form}:*\
                \n\
                \n*Банк:* {bank}\
                \n*{method}:* {account}\
                '''
    
    return reply_text


def response_sended(name, order_id):
    name = utils.escape_markdown(name)

    return f'Твой отклик на заявку {name} ({order_id}) *отправлен заказчику*.'


def response_declined_by_buyer(order_id, name):
    name = utils.escape_markdown(name)

    return f'Твой отклик на заявку {name} ({order_id}) отклонен пользователем.\n\nУправление откликами осуществляется в разделе *мои отклики*.'


def payment_declined_by_buyer(order_id, name):
    name = utils.escape_markdown(name)

    return f'Пользователь отказался от оплаты по отклику на заявку {name} ({order_id}).\n\nУправление откликами осуществляется в разделе *мои отклики*.'


def response_accepted_by_buyer(order_id, name):
    name = utils.escape_markdown(name)

    return f'Твой отклик на заявку {name} ({order_id}) принят пользователем, мы ожидаем поступление оплаты, о котором сразу тебя уведомим, после чего можешь приступать к выполнению заказа.\n\nУправление откликами осуществляется в разделе *мои отклики*.'


def seller_chosen(order_id, seller_username, name, price, delivery, comment):
    name = utils.escape_markdown(name)
    seller_username = utils.escape_markdown(seller_username)
    price_text = utils.numbers_format(price * (1 + config.PERCENT))
    percent = utils.numbers_format(price * config.PERCENT)
#FIXME:
    if delivery:
        delivery = 'включена'
    else:
        delivery = 'не включена'

    comment = utils.escape_markdown(comment)

    reply_text = f'''
                \nИсполнителем на заявку {name} ({order_id}) выбран @{seller_username} c предложением:\
                \n\
                \n*Стоимость:* {price_text} руб. (в т.ч. {percent} руб. - комиссия сервиса)\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                \n\
                \nДля того, чтоб исполнитель *приступил* к выполнению заказа:\
                \nПереведи сумму в *{price} руб.* по реквизитам и укажи в комментарии к платежу цифры *{order_id}*:\
                \n\
                \n*Банк:* Тинькофф\
                \n*Номер телефона:* 79641234567\
                \n\
                \nМы проверим поступление платежа, уведомим исполнителя - он получит средства только после выполнения своих обязательств.\
                \n\
                \nДля подтверждения платежа воспользуйся кнопкой *"оплачено"*, это можно сделать и позже в разделе *мои заявки*.\
                '''
    
    return reply_text


def response_paid(status, name, price, delivery, comment, order_id):
    name = utils.escape_markdown(name)
    price = utils.numbers_format(price)

    if delivery:
        delivery = 'включена в стоимость'
    else:
        delivery = 'не включена в стоимость'
    
    comment = utils.escape_markdown(comment)

    status_text = config.RESPONSES_STATUSES_LEGEND[status]

    reply_text = f'''
                \nОтклик на заявку {name} ({order_id}) помечен заказчиком как оплаченный:\
                \n\
                \n*{status_text}*\
                \n\
                \n*Цена:* {price} руб.\
                \n*Доставка:* {delivery}\
                \n*Комментарий:* {comment}\
                \n\
                \nМы проверим поступление платежа и сообщим в ближайшее время, после этого можно будет приступать к выполнению заказа.\
                \nСтатус отклика можно отслеживать в разделе *"мои отклики"*.\
                '''
    
    return reply_text


def verify_payment(price, order_id):
    price_text = utils.numbers_format(price * (1 + config.PERCENT))
    percent = utils.numbers_format(price * config.PERCENT)

    return f'Верифицируй платеж на сумму *{price_text} руб.*  (в т.ч. {percent} руб. - комиссия сервиса) по заявке {order_id}.'


def payment_verified_buyer(order_id, name):
    name = utils.escape_markdown(name)

    return f'Платеж по отклику на заявку {name} ({order_id}) *подтвержден администратором*.\nИсполнитель оповещен и уже приступил к выполнению заказа.'


def payment_verified_seller(order_id, name):
    name = utils.escape_markdown(name)

    return f'Платеж по отклику на заявку {name} ({order_id}) *подтвержден администратором*.\nМожно приступать к исполнению заказа, не забывай менять его статус в разделе "мои отклики".'


def payment_declined_buyer(order_id, name):
    name = utils.escape_markdown(name)

    return f'Платеж по отклику на заявку {name} ({order_id}) *не подтвержден администратором*.\nОтправь корректное подтверждение платежа через раздел *"мои заявки"*.'


def payment_declined_seller(order_id, name):
    name = utils.escape_markdown(name)

    return f'Платеж по отклику на заявку {name} ({order_id}) *не подтвержден администратором*.\nОтклик переведен в статус "ожидается оплата заказчиком", не приступай к выполнению заказа до получения уведомления.\nОтслеживать статус можно в разделе *"мои отклики"*.'


def received_confirm(order_id, name):
    name = utils.escape_markdown(name)

    return f'Товар по заявке {name} ({order_id}) *получен*?'


def bought_confirm(order_id, name):
    name = utils.escape_markdown(name)

    return f'Товар по заявке {name} ({order_id}) *куплен*?'


def sended_confirm(order_id, name):
    name = utils.escape_markdown(name)

    return f'Товар по заявке {name} ({order_id}) *отправлен*?'


def bought_product(order_id, name):
    name = utils.escape_markdown(name)

    return f'Исполнитель отметил товар по заявке {name} ({order_id}) как *купленный*, ожидаем подтверждения отправки.'


def sended_product(order_id, name):
    name = utils.escape_markdown(name)

    return f'Исполнитель отметил товар по заявке {name} ({order_id}) как *отправленный*, ожидаем подтверждение получения с твоей стороны.'


def received_product(order_id, name):
    name = utils.escape_markdown(name)

    return f'Покупатель отметил товар по заявке {name} ({order_id}) как *полученный*, мы переведем твое вознаграждение по указанным реквизитам и пришлем уведомление в ближайшее время!'


def transfer(order_id, name, payment_form, bank, account, price):
    name = utils.escape_markdown(name)

    if payment_form == 'sbp':
        payment_form = 'СБП (по номеру телефона)'
        method = 'Номер телефона'
    elif payment_form == 'card':
        payment_form = 'По номеру карты'
        method = 'Номер карты'

    bank = config.BANKS[bank]
    price = utils.numbers_format(price)

    reply_text = f'''
                \nЗаявка {name} ({order_id}) закрыта, реквизиты для перевода:\
                \n*{payment_form}:*\
                \n\
                \n*Банк:* {bank}\
                \n*{method}:* {account}\
                \n*Сумма:* {price} руб.\
                '''
    
    return reply_text


def transferred(order_id, name):
    name = utils.escape_markdown(name)
    
    return f'*Переведена оплата* за заявку {name} ({order_id}).'

    
#! ДЛЯ АДМИНИСТРАТОРОВ
INSPECT_OUTDATED = 'Прошло проверку или отменено пользователем.'

PAYMENT_OUTDATED = 'Прошло проверку.'

INSPECT_ORDER_CONFIRM = 'Заявка одобрена.'

INSPECT_ORDER_WHY_REJECTED = 'Укажите *причину отклонения* заявки.'

REJECTED_INFORMED = 'Пользователь оповещен об отклонении заявки.'

PAYMENT_CONFIRMED = 'Платеж подтвержден.'

PAYMENT_DECLINED = 'Платеж отклонен.'

TRANSFER_ALREADY = 'Выплата уже была совершена.'

SEND_CHECK = 'Отправь чек (скриншот), подтверждающий *платеж*.'

#! РАБОТА С ОТКЛИКОМ
CANCEL_RESPONSE_COMMAND = '\n\nВоспользуйся командой */cancel_response* если передумал и хочешь отменить отклик.'

CONFIRM_SKIPPING = '\n\nЕсли ты пропустишь эту заявку, то больше не сможешь на нее откликнуться, продолжить?'

CONFIRM_CANCEL_RESPONSE = '\n\nЕсли ты отменишь этот отклик, то больше не сможешь откликнуться на заявку, продолжить?'

ORDER_SKIPPED = '\n\nЗаявка пропущена.'

RESPONSE_CANCELED = 'Отклик *успешно* отменен.\nУправление откликами осуществляется в разделе *мои отклики*.'

RESPONSE_COMMENT = 'Укажи *комментарии к отклику*, воспользуйся командой */skip* для пропуска этого шага.' + CANCEL_RESPONSE_COMMAND

CHOOSE_PAYMENT_METHOD = 'Выбери *форму оплаты* для получения платежа:' + CANCEL_RESPONSE_COMMAND

CHOOSE_BANK = 'Выбери *банк* для получения платежа:' + CANCEL_RESPONSE_COMMAND

PHONE = 'Введи *номер телефона* для совершения перевода по СБП.\nВ формате: *79991234567*.' + CANCEL_RESPONSE_COMMAND

CARD = 'Введи *номер карты* для совершения перевода.\nВ формате: *5555 4444 3333 2222*.' + CANCEL_RESPONSE_COMMAND

CONFIRM_ACCEPT = '\n\nПосле подтверждения ты не сможешь принимать другие отклики на эту заявку, продолжить?'

CONFIRM_DECLINE = '\n\nТы больше не сможешь принять эту заявку, продолжить?'

RESPONSE_DECLINED = '\n\nОтклик отклонен.'

RESPONSE_OUTDATED = 'Отклик устарел.'

CANT_REVOKE = 'Невозможно отозвать отклик.'

WAITING_PAYMENT = 'Отправь скриншот, *подтверждающий платеж*. Для отмены ввода воспользуйся командой */cancel_input*.'

SEND_PAYMENT_CONFIRMATION = 'Отправить *подтверждение* платежа?'

RESPONSE_MARKED_PAID = 'Мы проверим поступление платежа и *пришлем уведомление*.\nСтатус заявки можно отслеживать в разделе "мои заявки".'

#! ОШИБКИ ПРИ СОЗДАНИИ ОТКЛИКА
UNFINISHED_RESPONSE = 'У тебя есть неподтвержденный отклик, прежде чем создавать новый воспользуйся командой */cancel_response* или подтверди предыдущий отклик.'

ORDER_OUTDATED_TO_RESPONSE = 'К сожалению, *заявка устарела*.'

USERNAME_NEEDED = 'Для отклика на заявку необходимо *заполненное имя пользователя*. Перейди в *настройки telegram*, задай имя пользователя и попробуй еще раз.\n\nНе удаляй имя пользователя, чтобы заказчик мог с тобой связаться для обсуждения деталей.'

WRONG_ACCOUNT_FORMAT = 'Введенные данные *не соответствуют формату*, попробуй еще раз.' + CANCEL_RESPONSE_COMMAND

ACCESS_DENIED = 'Недостаточно прав доступа.'

DATA_TRANSFERRED = 'Данные успешно перенесены.'