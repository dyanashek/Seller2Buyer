import re


# формат чисел
def numbers_format(value):
    """Makes a good looking numbers format."""

    if value:
        return '{:,}'.format(value).replace(',', ' ')
    else:
        return value


def validate_number(value):
    if value:
        value = value.replace(' ', '').replace(',', '.')

    try:
        value = float(value)
        return value

    except:
        return False


def escape_markdown(text):
    if text:
        characters_to_escape = ['_', '*', '[', ']', '`']
        for char in characters_to_escape:
            text = text.replace(char, '\\' + char)

    return text


def url_loc(lat, lon):
    url_loc = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}&accept-language=ru"

    return url_loc


def parse_user_info(user_info):
    name = escape_markdown(user_info[5])
    family_name = escape_markdown(user_info[6])
    phone = escape_markdown(user_info[7])

    if user_info[8]:
        phone += ' ✅'
    
    email = escape_markdown(user_info[11])
    country = escape_markdown(user_info[9])
    role = user_info[12]
    whole_world = user_info[14]

    return role, name, family_name, phone, email, country, whole_world


def validate_phone(phone):
    if phone:
        phone = phone.replace('(', '').replace(' ', '').replace(')', '').replace('-', '').replace('_', '').replace('+', '')

    try:
        if len(phone) == 11:
            int(phone)
            return phone

        else:
            return False

    except:
        return False


def validate_card(card):
    if card:
        card = card.replace(' ', '').replace('-', '').replace('_', '')

    try:
        if len(card) == 16:
            int(card)
            card = card[0:4] + ' ' + card[4:8] + ' ' + card[8:12] + ' ' + card[12:]
            return card

        else:
            return False

    except:
        return False