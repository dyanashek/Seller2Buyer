import os
import gspread
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_ID = os.getenv('BOT_ID')
MANAGER_ID = os.getenv('MANAGER_ID').split(', ')
MANAGER_USERNAME = os.getenv('MANAGER_USERNAME')

SPREAD_NAME = os.getenv('SPREAD_NAME')
USERS_LIST_NAME = os.getenv('USERS_LIST_NAME')
ORDERS_LIST_NAME = os.getenv('ORDERS_LIST_NAME')
RESPONSES_LIST_NAME = os.getenv('RESPONSES_LIST_NAME')

SERVICE_ACC = gspread.service_account(filename='service_account.json')
TABLE = SERVICE_ACC.open(SPREAD_NAME)

START_IMAGE = 'AgACAgIAAxkBAAMTZP6l-2-KHr6RD31yEX15V-rzntMAAo_LMRvbPOhLDE8HHFmCB5UBAAMCAAN5AAMwBA'

SAFETY = 'https://telegra.ph/Kak-my-garantiruem-bezopasnost-09-10'
ADVISE = 'https://telegra.ph/Rekomendacii-po-ispolzovaniyu-servisa-09-10'
INSTRUCTION = 'https://telegra.ph/Rekomendacii-po-ispolzovaniyu-servisa-09-10'

ON_PAGE = 5

PERCENT = 0.03

ROLES = {
    'покупатель' : 'buyer',
    'продавец' : 'seller',
}

ROLES_ENG = {
    'buyer' : 'Покупатель',
    'seller' : 'Продавец',
}

COUNTRIES = ('Россия', 'Казахстан', 'Украина', 'Грузия',)

ORDER_STATUSES = ['👨‍💼', '⛔️', '🔍', '💵', '💳', '🛍', '📦', '⏳', '✅', '❌']

RESPONSE_STATUSES = ['🔍', '⛔️', '❌', '💵', '💳', '🛍', '📦', '⏳', '💰', '✅']

REPLY_BUTTONS = ['Профиль', 'Мои заявки', 'Мои отклики', 'Помощь']

ORDERS_STATUSES_LEGEND = {
    'checking' : '👨‍💼 - заявка на рассмотрении у менеджера',
    'declined' : '⛔️ - не одобрена менеджером',
    'searching' : '🔍 - поиск исполнителя',
    'waiting_payment' : '💵 - ожидается оплата заказчиком',
    'waiting_confirm' : '💳 - ожидается верификация платежа',
    'waiting_buy' : '🛍 - ожидается подтверждение покупки',
    'waiting_departure' : '📦 - ожидается подтверждение отправки',
    'waiting_delivery' : '⏳ - ожидается доставка',
    'done' : '✅ - товар получен',
    'canceled' : '❌ - заявка отменена',
}

ORDERS_STATUSES_WITH_RESPONSE = ['waiting_payment', 'waiting_confirm', 'waiting_buy', 'waiting_departure', 'waiting_delivery', 'done']

RESPONSES_STATUSES_LEGEND = {
    'sended' : '🔍 - отправлен покупателю',
    'declined' : '⛔️ - отклонен покупателем',
    'canceled' : '❌ - отменен продавцом',
    'waiting_payment' : '💵 - ожидается оплата заказчиком',
    'waiting_confirm' : '💳 - ожидается верификация платежа',
    'waiting_buy' : '🛍 - ожидается подтверждение покупки',
    'waiting_departure' : '📦 - ожидается подтверждение отправки',
    'waiting_delivery' : '⏳ - ожидается доставка',
    'waiting_transfer' : '💰 - ожидается получение вознаграждения',
    'done' : '✅ - получена оплата',
}

BANKS = {
    'sber' : 'Сбер',
    'tinkoff' : 'Тинькофф',
    'vtb' : 'ВТБ',
    'open' : 'Открытие',
    'alfa' : 'Альфа-Банк',
    'raif' : 'Райффайзен Банк',
}