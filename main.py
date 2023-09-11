import telebot
import logging
import requests
import threading
import inspect

import config
import text
import db_functions
import utils
import functions
import keyboards


logging.basicConfig(level=logging.INFO, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'restart'])
def start_message(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id
    username = message.from_user.username

    if not db_functions.is_in_database(user_id):
        try:
            name = message.from_user.first_name.replace('_', ' ')
            family_name = message.from_user.last_name.replace('_', ' ')
        except:
            name = None
            family_name = None

        db_functions.add_user(user_id, username, name, family_name)

        bot.send_photo(chat_id=chat_id,
                       photo=config.START_IMAGE,
                       caption=text.WELCOME_MESSAGE,
                       reply_markup=keyboards.role_keyboard(),
                       parse_mode='Markdown',
                       disable_notification=True,
                       )

    else:
        if db_functions.get_field_info(user_id, 'checked_in'):

            role = db_functions.get_field_info(user_id, 'role')
            bot.send_message(chat_id=chat_id,
                            text=text.PROFILE_CONFIRM,
                            reply_markup=keyboards.main_keyboard(role),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )


#TODO: УДАЛИТЬ ПОСЛЕ ТЕСТА
@bot.message_handler(commands=['drop'])
def drop_message(message):
    db_functions.delete_user(message.from_user.id)
    bot.send_message(chat_id=message.chat.id,
                     text='Профиль удален.',
                     )


@bot.message_handler(commands=['profile'])
def profile_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    user_info = db_functions.get_users_all_info(user_id)
    reply = text.confirm_profile(*utils.parse_user_info(user_info))

    role = db_functions.get_field_info(user_id, 'role')

    bot.send_message(chat_id=chat_id,
                        text=reply,
                        reply_markup=keyboards.change_profile_keyboard(role, False),
                        parse_mode='Markdown',
                        disable_notification=True,
                        )


@bot.message_handler(commands=['cancel'])
def drop_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if db_functions.get_field_info(user_id, 'checked_in') and db_functions.get_field_info(user_id, 'input'):
        if db_functions.get_field_info(user_id, 'input_data') == 'country' and db_functions.get_field_info(user_id, 'role') == 'seller'\
        and not db_functions.get_field_info(user_id, 'country_verified'):
            bot.send_message(chat_id=chat_id,
                                text=text.LOCATION_NEEDED,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        else:
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)

            user_info = db_functions.get_users_all_info(user_id)
            reply = text.confirm_profile(*utils.parse_user_info(user_info))

            role = db_functions.get_field_info(user_id, 'role')

            bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )


@bot.message_handler(commands=['cancel_order'])
def drop_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    db_functions.update_field(user_id, 'input', False)
    db_functions.update_field(user_id, 'input_data', None)

    db_functions.delete_order(user_id)

    bot.send_message(chat_id=chat_id,
                     text=text.ORDER_CANCELED,
                     parse_mode='Markdown',
                     disable_notification=True,
                     )


@bot.message_handler(commands=['cancel_response'])
def drop_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    db_functions.update_field(user_id, 'input', False)
    db_functions.update_field(user_id, 'input_data', None)

    db_functions.delete_response(user_id)

    bot.send_message(chat_id=chat_id,
                     text=text.RESPONSE_CANCELED,
                     parse_mode='Markdown',
                     disable_notification=True,
                     )


@bot.message_handler(commands=['skip'])
def skip_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    input_info = db_functions.get_input_status(user_id)

    # пользователь в режиме ввода информации
    if input_info[0]:
        input_data = input_info[1]

        if input_data == 'order_comment':
            db_functions.update_order_field(user_id, 'comment', '-')
            order_status = db_functions.get_order_field_info(user_id, 'status')
            
            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_country')

                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_COUNTRY,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=text.confirm_order(*order_info),
                               reply_markup=keyboards.change_order_keyboard(),
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
        
        elif input_data == 'order_country':
            db_functions.update_order_field(user_id, 'country', '-')
            order_status = db_functions.get_order_field_info(user_id, 'status')
            
            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_link')
                
                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_LINK,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=text.confirm_order(*order_info),
                               reply_markup=keyboards.change_order_keyboard(),
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
        
        elif input_data == 'order_link':
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_order_field(user_id, 'link', '-')
            db_functions.update_order_field(user_id, 'status', 'created')

            order_info = db_functions.get_order_info(user_id)
            photo_id = order_info[2]

            bot.send_photo(chat_id=chat_id,
                           photo=photo_id,
                           caption=text.confirm_order(*order_info),
                           reply_markup=keyboards.change_order_keyboard(),
                           parse_mode='Markdown',
                           disable_notification=True,
                           )
        
        elif input_data == 'response_comment':
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_response_field(user_id, 'comment', '-')
            db_functions.update_response_field(user_id, 'status', 'created')

            response_info = db_functions.get_response_info(user_id)

            bot.send_message(chat_id=chat_id,
                             text=text.confirm_response(*response_info),
                             reply_markup=keyboards.change_response_keyboard(),
                             parse_mode='Markdown',
                             )


@bot.message_handler(commands=['help'])
def skip_message(message):
    chat_id = message.chat.id

    bot.send_message(chat_id=chat_id,
                     text=text.HELP,
                     reply_markup=keyboards.manager_keyboard(),
                     parse_mode='Markdown',
                     disable_notification=True,
                     )


@bot.message_handler(commands=['cancel_input'])
def skip_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    input_info = db_functions.get_input_status(user_id)

    if input_info[0] and 'order-payment' in input_info[1]:
        db_functions.update_field(user_id, 'input', False)
        db_functions.update_field(user_id, 'input_data', None)

        bot.send_message(chat_id=chat_id,
                         text=text.INPUT_CANCELED,
                         parse_mode='Markdown',
                         disable_notification=True,
                         )


@bot.message_handler(commands=['google'])
def drop_message(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    if user_id in config.MANAGER_ID:
        threading.Thread(daemon=True, target=functions.data_to_google, args=(user_id,)).start()
    else:
        bot.send_message(chat_id=chat_id,
                         text=text.ACCESS_DENIED,
                         )


@bot.message_handler(commands=['log'])
def start_message(message):
    user_id = str(message.from_user.id)

    if user_id in config.MANAGER_ID:
            threading.Thread(daemon=True, 
                        target=functions.send_log, 
                        args=(user_id,),
                        ).start()
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=text.ACCESS_DENIED,
                         )


@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    call_data = call.data.split('_')
    query = call_data[0]

    if query == 'confirm':
        data = call_data[1].replace('-', '_')
        
        if data == 'name':
            input_info = db_functions.get_input_status(user_id)

            # пользователь в режиме ввода информации, вводит имя
            if input_info[0] and input_info[1] == 'name':
                db_functions.update_field(user_id, 'input_data', 'family_name')

                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )
                
                family_name = db_functions.get_field_info(user_id, 'family_name')

                # если фамилия в профиле заполнена
                if family_name:
                    bot.send_message(chat_id=chat_id,
                                        text=text.confirm_family_name(family_name),
                                        reply_markup=keyboards.confirm_data_keyboard('family-name'),
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )

                # если фамилия в профиле не заполнена
                else:
                    bot.send_message(chat_id=chat_id,
                                        text=text.ASK_FAMILY_NAME,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )

            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.OUTDATED_MESSAGE,
                                      )

        elif data == 'family_name':
            input_info = db_functions.get_input_status(user_id)

            # пользователь в режиме ввода информации, вводит имя
            if input_info[0] and input_info[1] == 'family_name':
                db_functions.update_field(user_id, 'input_data', 'phone')

                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )

                bot.send_message(chat_id=chat_id,
                                 text=text.ASK_PHONE,
                                 reply_markup=keyboards.request_phone_keyboard(),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
                
            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.OUTDATED_MESSAGE,
                                      )
        
        elif data == 'profile':
            role = db_functions.get_field_info(user_id, 'role')

            bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )

            bot.send_message(chat_id=chat_id,
                             text=text.PROFILE_CONFIRM,
                             reply_markup=keyboards.main_keyboard(role),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
            
            if role == 'seller':
                if db_functions.get_field_info(user_id, 'settings'):
                    orders_ids = db_functions.select_unfinished_orders_whole_world(user_id)
                else:
                    country = db_functions.get_field_info(user_id, 'country')
                    orders_ids = db_functions.select_unfinished_orders_location_country(user_id, country)
                
                if orders_ids:
                    threading.Thread(daemon=True, target=functions.notify_seller_unfinished_orders, args=(user_id, orders_ids,)).start()

        elif data == 'address':
            order_status = db_functions.get_order_field_info(user_id, 'status')

            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_name')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.PRODUCT_NAME,
                                      parse_mode='Markdown',
                                      )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)

                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                                photo=photo_id,
                                caption=text.confirm_order(*order_info),
                                reply_markup=keyboards.change_order_keyboard(),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        elif data == 'order':
            order_id = db_functions.get_order_field_info(user_id, 'id')
            db_functions.update_order_field(user_id, 'status', 'checking')

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                             text=text.SEND_TO_ADMIN,
                             parse_mode='Markdown',
                             reply_markup=keyboards.view_order_keyboard(order_id),
                             disable_notification=True,
                             )

            threading.Thread(daemon=True, target=functions.order_to_inspect_by_admins, args=(order_id,)).start()

        elif data == 'response':
            order_id = db_functions.get_response_field_info(user_id, 'order_id')

            if db_functions.get_field_info_by_order_id(order_id, 'status') == 'searching':
                username = call.from_user.username

                if username:
                    db_functions.update_field(user_id, 'username', username)
                    name = db_functions.get_response_field_info(user_id, 'name')
                    response_id = db_functions.get_response_field_info(user_id, 'id')
                    buyer_id = db_functions.get_response_field_info(user_id, 'buyer')
                    response_info = db_functions.get_response_info(user_id)

                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text=text.response_sended(name, order_id),
                                          parse_mode='Markdown',
                                          )
                    
                    bot.edit_message_reply_markup(chat_id=chat_id,
                                                  message_id=message_id,
                                                  reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                                  )

                    try:
                        bot.send_message(chat_id=buyer_id,
                                        text=text.get_response(username, *response_info),
                                        reply_markup=keyboards.get_response_keyboard(response_id, order_id),
                                        parse_mode='Markdown',
                                        )
                    except Exception as ex:
                        logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить отклик ({user_id}) пользователю ({buyer_id}). {ex}')
                    
                    db_functions.update_response_field(user_id, 'status', 'sended')

                else:
                    bot.send_message(chat_id=chat_id,
                                     text=text.USERNAME_NEEDED,
                                     parse_mode='Markdown',
                                     )
            
            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.ORDER_OUTDATED_TO_RESPONSE,
                                      parse_mode='Markdown',
                                      )

    elif query == 'cancel':
        data = call_data[1]

        if data == 'order':
            db_functions.delete_order(user_id)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                             text=text.ORDER_CANCELED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
        
        if data == 'response':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text + text.CONFIRM_CANCEL_RESPONSE,
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.confirm_cancel_response_keyboard(),
                                          )

    elif query == 'delete':
        action = call_data[1]

        if action == 'confirm':
            db_functions.delete_response(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.RESPONSE_CANCELED,
                                  parse_mode='Markdown',
                                  )
        
        elif action == 'cancel':
            response_info = db_functions.get_response_info(user_id)
            
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.confirm_response(*response_info),
                                  parse_mode='Markdown',
                                  )
            
            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.change_response_keyboard(),
                                          )

    elif query == 'decline':
        data = call_data[1]

        if data == 'address':
            addresses = eval(db_functions.get_field_info(user_id, 'addresses'))
            del addresses[-1]

            db_functions.update_field(user_id, 'addresses', str(addresses))
            db_functions.update_order_field(user_id, 'address', None)

            reply_text = text.INPUT_ADDRESS
            if addresses:
                reply_text = text.INPUT_OR_CHOOSE_ADDRESS
            
            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )
            
            if addresses:
                bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=message_id,
                                                reply_markup=keyboards.addresses_keyboard(addresses),
                                                )

    elif query == 'settings':
        world_setting = call_data[1]

        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'settings':
            if world_setting == 'country':
                db_functions.update_field(user_id, 'settings', False)
            elif world_setting == 'whole':
                db_functions.update_field(user_id, 'settings', True)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            if not db_functions.get_field_info(user_id, 'checked_in'):
                db_functions.update_field(user_id, 'input_data', 'name')
                name = db_functions.get_field_info(user_id, 'name')

                # если имя в профиле заполнено
                if name:
                    bot.send_message(chat_id=chat_id,
                                        text=text.confirm_name(name),
                                        reply_markup=keyboards.confirm_data_keyboard('name'),
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
                                        
                # если имя в профиле не заполнено
                else:
                    bot.send_message(chat_id=chat_id,
                                        text=text.ASK_NAME,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )

            else:
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.OUTDATED_MESSAGE,
                                    )

    elif query == 'country':
        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'country':

            bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )

            country = call_data[1].lower()

            db_functions.update_field(user_id, 'country', country)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'checked_in', True)

            user_info = db_functions.get_users_all_info(user_id)
            reply = text.confirm_profile(*utils.parse_user_info(user_info))

            role = db_functions.get_field_info(user_id, 'role')

            bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        else:
            bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.OUTDATED_MESSAGE,
                                    )

    elif query == 'change':
        area = call_data[1]
        subject = call_data[2].replace('-', '_')

        if area == 'profile':
            db_functions.update_field(user_id, 'input', True)
            db_functions.update_field(user_id, 'input_data', subject)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            if subject == 'name':
                bot.send_message(chat_id=chat_id,
                                        text=text.ASK_NAME + text.CANCEL_COMMAND,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
            
            elif subject == 'family_name':
                bot.send_message(chat_id=chat_id,
                                        text=text.ASK_FAMILY_NAME + text.CANCEL_COMMAND,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
            
            elif subject == 'phone':
                bot.send_message(chat_id=chat_id,
                                    text=text.ASK_PHONE + text.CANCEL_COMMAND,
                                    reply_markup=keyboards.request_phone_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
            
            elif subject == 'email':
                bot.send_message(chat_id=chat_id,
                                        text=text.ASK_EMAIL + text.CANCEL_COMMAND,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
            
            elif subject == 'role':
                if db_functions.get_field_info(user_id, 'role') == 'seller' and db_functions.check_unfinished_responses(user_id):
                    bot.send_message(chat_id=chat_id,
                                text=text.CANT_CHANGE_ROLE,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

                else:
                    bot.send_message(chat_id=chat_id,
                                text=text.ROLE_WRONG_INPUT + text.CANCEL_COMMAND,
                                reply_markup=keyboards.role_keyboard(),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif subject == 'country':
                role = db_functions.get_field_info(user_id, 'role')
                if role == 'buyer':
                    bot.send_message(chat_id=chat_id,
                                    text=text.ASK_COUNTRY_BUYER  + text.CANCEL_COMMAND,
                                    reply_markup=keyboards.countries_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
                
                elif role == 'seller':
                    bot.send_message(chat_id=chat_id,
                                    text=text.ASK_COUNTRY_SELLER  + text.CANCEL_COMMAND,
                                    reply_markup=keyboards.request_country_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
            
            elif subject == 'settings':
                bot.send_message(chat_id=chat_id,
                                 text=text.WHOLE_WORLD,
                                 reply_markup=keyboards.settings_keyboard(),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
        
        elif area == 'order':
            db_functions.update_field(user_id, 'input', True)

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            if subject == 'address':
                db_functions.update_field(user_id, 'input_data', 'address')

                addresses = eval(db_functions.get_field_info(user_id, 'addresses'))

                reply_text = text.INPUT_ADDRESS
                if addresses:
                    reply_text = text.INPUT_OR_CHOOSE_ADDRESS

                bot.send_message(chat_id=chat_id,
                                 text=reply_text,
                                 reply_markup=keyboards.addresses_keyboard(addresses),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
            
            elif subject == 'name':
                db_functions.update_field(user_id, 'input_data', 'order_name')

                bot.send_message(chat_id=chat_id,
                                      text=text.PRODUCT_NAME,
                                      parse_mode='Markdown',
                                      disable_notification=True,
                                      )
            
            elif subject == 'photo':
                db_functions.update_field(user_id, 'input_data', 'order_photo')

                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_PHOTO,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif subject == 'comment':
                db_functions.update_field(user_id, 'input_data', 'order_comment')

                bot.send_message(chat_id=chat_id,
                                    text=text.PRODUCT_COMMENT,
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
            
            elif subject == 'country':
                db_functions.update_field(user_id, 'input_data', 'order_country')

                bot.send_message(chat_id=chat_id,
                                    text=text.PRODUCT_COUNTRY,
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
            
            elif subject == 'link':
                db_functions.update_field(user_id, 'input_data', 'order_link')

                bot.send_message(chat_id=chat_id,
                                    text=text.PRODUCT_LINK,
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
        
        elif area == 'response':
            db_functions.update_field(user_id, 'input', True)

            if subject == 'price':
                db_functions.update_field(user_id, 'input_data', 'price')

                name = db_functions.get_response_field_info(user_id, 'name')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.ask_response_price(name),
                                      parse_mode='Markdown',
                                      )

            elif subject == 'delivery':
                db_functions.update_field(user_id, 'input_data', 'delivery')

                name = db_functions.get_response_field_info(user_id, 'name')
                price = db_functions.get_response_field_info(user_id, 'price')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.ask_delivery(name, price),
                                      parse_mode='Markdown',
                                      )
                
                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=keyboards.delivery_keyboard(),
                                              )

            elif subject == 'comment':
                db_functions.update_field(user_id, 'input_data', 'response_comment')

                bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.RESPONSE_COMMENT,
                                  parse_mode='Markdown',
                                  )

    elif query == 'close':
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )
    
    elif query == 'new':
        subject = call_data[1]

        if subject == 'order':
            if not db_functions.select_creating_orders(user_id):
                db_functions.add_order(user_id)

                addresses = eval(db_functions.get_field_info(user_id, 'addresses'))

                db_functions.update_field(user_id, 'input', True)
                db_functions.update_field(user_id, 'input_data', 'address')

                reply_text = text.INPUT_ADDRESS
                if addresses:
                    reply_text = text.INPUT_OR_CHOOSE_ADDRESS
                
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=reply_text,
                                    parse_mode='Markdown',
                                    )
                
                if addresses:
                    bot.edit_message_reply_markup(chat_id=chat_id,
                                                  message_id=message_id,
                                                  reply_markup=keyboards.addresses_keyboard(addresses),
                                                  )
            
            else:
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.UNFINISHED_ORDER,
                                    parse_mode='Markdown',
                                    )
    
    elif query == 'address':
        index = int(call_data[1])
        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'address':

            addresses = eval(db_functions.get_field_info(user_id, 'addresses'))
            db_functions.update_order_field(user_id, 'address', addresses[index])

            order_status = db_functions.get_order_field_info(user_id, 'status')

            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_name')

                bot.edit_message_text(chat_id=chat_id,
                                        message_id=message_id,
                                        text=text.PRODUCT_NAME,
                                        parse_mode='Markdown',
                                        )

            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass

                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                                photo=photo_id,
                                caption=text.confirm_order(*order_info),
                                reply_markup=keyboards.change_order_keyboard(),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED_MESSAGE,
                                  parse_mode='Markdown',
                                  )

    elif query == 'filter':
        area = call_data[1]
        filter_status = call_data[2]

        if area == 'orders':
            current_order_filter = db_functions.get_field_info(user_id, 'orders_filter')

            if filter_status == current_order_filter:
                db_functions.update_field(user_id, 'orders_filter', 'all')
                filter_status = 'all'
            else:
                db_functions.update_field(user_id, 'orders_filter', filter_status)

            orders = db_functions.select_user_orders(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.orders_legend(filter_status),
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.orders_keyboard(orders, 1, filter_status),
                                          )
        
        elif area == 'responses':
            current_response_filter = db_functions.get_field_info(user_id, 'responses_filter')

            if filter_status == current_response_filter:
                db_functions.update_field(user_id, 'responses_filter', 'all')
                filter_status = 'all'
            else:
                db_functions.update_field(user_id, 'responses_filter', filter_status)

            responses = db_functions.select_user_responses(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.responses_legend(filter_status),
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.responses_keyboard(responses, 1, filter_status),
                                          )

    elif query == 'page':
        area = call_data[1]
        page = int(call_data[2])

        if area == 'order':
            filter_status = db_functions.get_field_info(user_id, 'orders_filter')
            orders = db_functions.select_user_orders(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.orders_legend(filter_status),
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.orders_keyboard(orders, page, filter_status),
                                          )
        elif area == 'response':
            filter_status = db_functions.get_field_info(user_id, 'responses_filter')
            responses = db_functions.select_user_responses(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.responses_legend(filter_status),
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.responses_keyboard(responses, page, filter_status),
                                          )

    elif query == 'order':
        order_id = int(call_data[1])
        page = int(call_data[2])

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        order_info = db_functions.get_order_info_by_order_id(order_id)
        status = order_info[0]
        photo_id = order_info[4]

        reply_text = text.order_info(order_id, *order_info)

        bot.send_photo(chat_id=chat_id,
                       photo=photo_id,
                       caption=reply_text,
                       reply_markup=keyboards.order_keyboard(page, status, order_id),
                       parse_mode='Markdown',
                       disable_notification=True,
                       )

    elif query == 'respond':
        response_id = int(call_data[1])
        page = int(call_data[2])
        
        response_info = db_functions.get_response_info_by_response_id(response_id)
        status = response_info[0]
        order_id = response_info[5]

        reply_text = text.response_info(*response_info)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=reply_text,
                              parse_mode='Markdown',
                              )

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.response_keyboard(page, status, response_id, order_id),
                                      )

    elif query == 'revoke':
        area = call_data[1]

        if area == 'order':
            order_id = int(call_data[2])

            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass
            
            prev_status = db_functions.get_field_info_by_order_id(order_id, 'status')
            db_functions.update_field_by_order_id(order_id, 'status', 'canceled')

            bot.send_message(chat_id=chat_id,
                             text=text.ORDER_CANCELED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

            if prev_status == "waiting_payment":
                response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
                db_functions.update_field_by_response_id(response_id, 'status', 'canceled')

                seller_id = db_functions.get_field_info_by_order_id(order_id, 'seller')
                name = db_functions.get_field_info_by_order_id(order_id, 'name')

                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.payment_declined_by_buyer(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {seller_id} об отклонении отклика {response_id}. {ex}')
        
        elif area == 'response':
            response_id = int(call_data[2])
            page = int(call_data[3])

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text + text.CONFIRM_CANCEL_RESPONSE,
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.confirm_revoke_response_keyboard(response_id, page)
                                          )

    elif query == 'back':
        destination = call_data[1]
        page = int(call_data[2])

        if destination == 'orders':
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            filter_status = db_functions.get_field_info(user_id, 'orders_filter')
            orders = db_functions.select_user_orders(user_id)

            bot.send_message(chat_id=chat_id,
                             text=text.orders_legend(filter_status),
                             reply_markup=keyboards.orders_keyboard(orders, page, filter_status),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
        
        elif destination == 'method':
            input_info = db_functions.get_input_status(user_id)

            if input_info[0] and input_info[1] == 'bank':
                db_functions.update_field(user_id, 'payment_form', None)
                db_functions.update_field(user_id, 'input_data', 'payment_form')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.CHOOSE_PAYMENT_METHOD,
                                      parse_mode='Markdown',
                                      )
                
                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=keyboards.payment_method_keyboard(),
                                              )

            else:
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.OUTDATED_MESSAGE,
                                    parse_mode='Markdown',
                                    )

        elif destination == 'responses':
            filter_status = db_functions.get_field_info(user_id, 'responses_filter')
            responses = db_functions.select_user_responses(user_id)

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.responses_legend(filter_status),
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.responses_keyboard(responses, page, filter_status),
                                          )
        
        elif destination == 'response':
            response_id = int(call_data[3])

            response_info = db_functions.get_response_info_by_response_id(response_id)
            status = response_info[0]
            order_id = response_info[5]

            reply_text = text.response_info(*response_info)

            bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=reply_text,
                                parse_mode='Markdown',
                                )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=keyboards.response_keyboard(page, status, response_id, order_id),
                                        )

    elif query == 'inspect':
        decision = call_data[1]
        order_id = int(call_data[2])
        buyer_id = int(call_data[3])

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        if db_functions.get_field_info_by_order_id(order_id, 'status') == 'checking':
            if decision == 'confirm':
                db_functions.update_field_by_order_id(order_id, 'status', 'searching')
                db_functions.update_field_by_order_id(order_id, 'approved_by', user_id)

                name = db_functions.get_field_info_by_order_id(order_id, 'name')

                bot.send_message(chat_id=chat_id,
                                  text=text.INSPECT_ORDER_CONFIRM,
                                  parse_mode='Markdown',
                                  )
                try:
                    bot.send_message(chat_id=buyer_id,
                                     text=text.order_inspected_confirm(order_id, name),
                                     reply_markup=keyboards.view_order_keyboard(order_id),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось уведомить пользователя {buyer_id} о одобрении заявки {order_id}. {ex}')

                threading.Thread(daemon=True, target=functions.notify_sellers_new_order, args=(order_id, buyer_id,)).start()

            elif decision == 'reject':
                db_functions.update_field_by_order_id(order_id, 'status', 'declined')
                db_functions.update_field_by_order_id(order_id, 'approved_by', user_id)
                db_functions.update_field(user_id, 'input', True)
                db_functions.update_field(user_id, 'input_data', f'reason_{order_id}')

                bot.send_message(chat_id=chat_id,
                                 text=text.INSPECT_ORDER_WHY_REJECTED,
                                 parse_mode='Markdown',
                                 )

        else:
            bot.send_message(chat_id=chat_id,
                             text=text.INSPECT_OUTDATED,
                             parse_mode='Markdown',
                             )

    elif query == 'response':
        action = call_data[1]
        order_id = int(call_data[2])

        if db_functions.get_field_info_by_order_id(order_id, 'status') == 'searching':
            if db_functions.get_field_info(user_id, 'role') == 'seller':
                if action == 'skip':
                    bot.edit_message_caption(chat_id=chat_id,
                                            message_id=message_id,
                                            caption=call.message.caption + text.CONFIRM_SKIPPING,
                                            )
                    
                    bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=message_id,
                                                reply_markup=keyboards.confirm_skip_order_keyboard(order_id),
                                                )
                
                elif action == 'confirm':
                    if not db_functions.select_creating_responses(user_id):
                        buyer_id = db_functions.get_field_info_by_order_id(order_id, 'buyer')
                        name = db_functions.get_field_info_by_order_id(order_id, 'name')

                        payment_form = db_functions.get_field_info(user_id, 'payment_form')
                        bank = db_functions.get_field_info(user_id, 'bank')
                        account = db_functions.get_field_info(user_id, 'account')

                        db_functions.add_response(order_id, user_id, buyer_id, name, payment_form, bank, account)

                        bot.edit_message_reply_markup(chat_id=chat_id,
                                                      message_id=message_id,
                                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                                      )
                    
                        if payment_form and bank and account:
                            db_functions.update_field(user_id, 'input', True)
                            db_functions.update_field(user_id, 'input_data', 'account')
                            bot.send_message(chat_id=chat_id,
                                             text=text.confirm_bank_account(payment_form, bank, account),
                                             reply_markup=keyboards.confirm_account_keyboard(),
                                             parse_mode='Markdown',
                                             )
                        
                        else:
                            db_functions.update_field(user_id, 'input', True)
                            db_functions.update_field(user_id, 'input_data', 'payment_form')

                            bot.send_message(chat_id=chat_id,
                                             text=text.CHOOSE_PAYMENT_METHOD,
                                             reply_markup=keyboards.payment_method_keyboard(),
                                             parse_mode='Markdown',
                                             )

                    else:
                        bot.send_message(chat_id=chat_id,
                                        text=text.UNFINISHED_RESPONSE,
                                        parse_mode='Markdown',
                                        )
                    
            else:
                try:
                    bot.delete_message(chat_id, message_id)
                except:
                    pass

                bot.send_message(chat_id=chat_id,
                                text=text.RESPONSE_ORDER_ROLE_ERROR,
                                parse_mode='Markdown',
                                )
        
        else:
            try:
                bot.delete_message(chat_id, message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                            text=text.ORDER_OUTDATED_TO_RESPONSE,
                            parse_mode='Markdown',
                            )
    
    elif query == 'method':
        method = call_data[1]
        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'payment_form':
            db_functions.update_field(user_id, 'payment_form', method)
            db_functions.update_field(user_id, 'input_data', 'bank')

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.CHOOSE_BANK,
                                  parse_mode='Markdown',
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.banks_keyboard(),
                                          )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED_MESSAGE,
                                  parse_mode='Markdown',
                                  )

    elif query == 'bank':
        bank = call_data[1]
        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'bank':
            db_functions.update_field(user_id, 'bank', bank)
            
            payment_method = db_functions.get_field_info(user_id, 'payment_form')

            if payment_method == 'card':
                db_functions.update_field(user_id, 'input_data', 'account_card')
                bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.CARD,
                                  parse_mode='Markdown',
                                  )

            elif payment_method == 'sbp':
                db_functions.update_field(user_id, 'input_data', 'account_phone')
                bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.PHONE,
                                  parse_mode='Markdown',
                                  )
        
        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED_MESSAGE,
                                  parse_mode='Markdown',
                                  )

    elif query == 'skip':
        action = call_data[1]
        order_id = int(call_data[2])

        if action == 'confirm':
            bot.edit_message_caption(chat_id=chat_id,
                                         message_id=message_id,
                                         caption=call.message.caption.replace(text.CONFIRM_SKIPPING, text.ORDER_SKIPPED),
                                         )
        
        elif action == 'cancel':
            bot.edit_message_caption(chat_id=chat_id,
                                     message_id=message_id,
                                     caption=call.message.caption.replace(text.CONFIRM_SKIPPING, ''),
                                     )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.response_order_keyboard(order_id),
                                          )

    elif query == 'delivery':
        param = call_data[1]   

        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'delivery':

            if param == 'include':
                db_functions.update_response_field(user_id, 'delivery', True)
            elif param == 'no':
                db_functions.update_response_field(user_id, 'delivery', False)  

            response_status = db_functions.get_response_field_info(user_id, 'status')

            if response_status == 'creating':                       
                db_functions.update_field(user_id, 'input_data', 'response_comment')

                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.RESPONSE_COMMENT,
                                    parse_mode='Markdown',
                                    )

            elif response_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)

                response_info = db_functions.get_response_info(user_id)

                bot.send_message(chat_id=chat_id,
                                text=text.confirm_response(*response_info),
                                reply_markup=keyboards.change_response_keyboard(),
                                parse_mode='Markdown',
                                )
        
        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED_MESSAGE,
                                  parse_mode='Markdown',
                                  )

    elif query == 'account':
        action = call_data[1]

        input_info = db_functions.get_input_status(user_id)

        if input_info[0] and input_info[1] == 'account':
            if action == 'confirm':
                payment_form = db_functions.get_field_info(user_id, 'payment_form')
                bank = db_functions.get_field_info(user_id, 'bank')
                account = db_functions.get_field_info(user_id, 'account')

                db_functions.update_response_field(user_id, 'payment_form', payment_form)
                db_functions.update_response_field(user_id, 'bank', bank)
                db_functions.update_response_field(user_id, 'account', account)

                db_functions.update_field(user_id, 'input_data', 'price')

                name = db_functions.get_response_field_info(user_id, 'name')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.ask_response_price(name),
                                      parse_mode='Markdown',
                                      )
            
            elif action == 'reenter':
                db_functions.update_field(user_id, 'payment_form', None)
                db_functions.update_field(user_id, 'bank', None)
                db_functions.update_field(user_id, 'account', None)

                db_functions.update_field(user_id, 'input_data', 'payment_form')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.CHOOSE_PAYMENT_METHOD,
                                      parse_mode='Markdown',
                                      )
                
                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=keyboards.payment_method_keyboard(),
                                              )

        else:
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.OUTDATED_MESSAGE,
                                  parse_mode='Markdown',
                                  )
    
    elif query == 'view':
        subject = call_data[1]

        if subject == 'order':
            order_id = int(call_data[2])

            order_info = db_functions.get_order_info_by_order_id(order_id)
            photo_id = order_info[4]

            reply_text = text.order_info(order_id, *order_info)

            bot.send_photo(chat_id=chat_id,
                        photo=photo_id,
                        caption=reply_text,
                        parse_mode='Markdown',
                        disable_notification=True,
                        )
        
        elif subject == 'response':
            response_id = int(call_data[2])
            instance = call_data[3]

            response_info = db_functions.get_response_info_by_response_id(response_id)


            if instance == 'my':
                bot.send_message(chat_id=chat_id,
                                 text=text.response_info(*response_info),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )

            elif instance == 'others':
                seller_id = db_functions.get_field_info_by_response_id(response_id, 'seller')
                seller_username = db_functions.get_field_info(seller_id, 'username')

                bot.send_message(chat_id=chat_id,
                                 text=text.others_response_info(seller_username, *response_info),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )
    
    elif query == 'deal':
        action = call_data[1]
        response_id = int(call_data[2])

        if action == 'accept':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text + text.CONFIRM_ACCEPT,
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.confirm_accept_keyboard(response_id),
                                          )

        elif action == 'decline':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text + text.CONFIRM_DECLINE,
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.confirm_decline_keyboard(response_id),
                                          )

    elif query == 'annul':
        action = call_data[1]
        response_id = int(call_data[2])
        order_id = db_functions.get_field_info_by_response_id(response_id, 'order_id')

        if action == 'confirm':
            if db_functions.get_field_info_by_response_id(response_id, 'status') == 'sended':
                db_functions.update_field_by_response_id(response_id, 'status', 'declined')

                seller_id = db_functions.get_field_info_by_response_id(response_id, 'seller')
                name = db_functions.get_field_info_by_response_id(response_id, 'name')

                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.response_declined_by_buyer(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {seller_id} об отклонении отклика {response_id}. {ex}')

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text.replace(text.CONFIRM_DECLINE, text.RESPONSE_DECLINED),
                                  )
        
        elif action == 'cancel':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text.replace(text.CONFIRM_DECLINE, ''),
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.get_response_keyboard(response_id, order_id),
                                          )
    
    elif query == 'accept':
        action = call_data[1]
        response_id = int(call_data[2])
        response_info = db_functions.get_response_info_by_response_id(response_id)
        order_id = response_info[5]

        if action == 'confirm':
            if db_functions.get_field_info_by_response_id(response_id, 'status') == 'sended':
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_payment')
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_payment')

                seller_id = db_functions.get_field_info_by_response_id(response_id, 'seller')
                db_functions.update_field_by_order_id(order_id, 'seller', seller_id)
                db_functions.update_field_by_order_id(order_id, 'response_id', response_id)
                
                name = response_info[1]
                price = response_info[2]
                delivery = response_info[3]
                comment = response_info[4]
                seller_username = db_functions.get_field_info(seller_id, 'username')

                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.response_accepted_by_buyer(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {seller_id} о принятии отклика {response_id}. {ex}')

                

                bot.edit_message_reply_markup(chat_id=chat_id,
                                              message_id=message_id,
                                              reply_markup=telebot.types.InlineKeyboardMarkup(),
                                              )
                
                bot.send_message(chat_id=chat_id,
                                text=text.seller_chosen(order_id, seller_username, name, price, delivery, comment),
                                reply_markup=keyboards.order_paid(order_id),
                                parse_mode='Markdown',
                                )
            
            else:
                bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=text.RESPONSE_OUTDATED,
                                  parse_mode='Markdown',
                                  )

        elif action == 'cancel':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text.replace(text.CONFIRM_ACCEPT, ''),
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.get_response_keyboard(response_id, order_id),
                                          )

    elif query == 'void':
        action = call_data[1]
        response_id = int(call_data[2])
        page = int(call_data[3])

        if action == 'confirm':
            if db_functions.get_field_info_by_response_id(response_id, 'status') == 'sended':
                db_functions.update_field_by_response_id(response_id, 'status', 'canceled')

                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.RESPONSE_CANCELED,
                                    parse_mode='Markdown',
                                    )
            else:
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=text.CANT_REVOKE,
                                    parse_mode='Markdown',
                                    )
        
        elif action == 'cancel':
            order_id = db_functions.get_field_info_by_response_id(response_id, 'order_id')
            status = db_functions.get_field_info_by_response_id(response_id, 'status_id')

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=call.message.text.replace(text.CONFIRM_CANCEL_RESPONSE, ''),
                                  )

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=keyboards.response_keyboard(page, status, response_id, order_id),
                                          )

    elif query == 'paid':
        area = call_data[1]

        if area == 'order':
            order_id = int(call_data[2])

            db_functions.update_field(user_id, 'input', True)
            db_functions.update_field(user_id, 'input_data', f'order-payment_{order_id}')

            bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=message_id,
                                          reply_markup=telebot.types.InlineKeyboardMarkup(),
                                          )

            bot.send_message(chat_id=chat_id,
                             text=text.WAITING_PAYMENT,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

    elif query == 'payment-photo':
        action = call_data[1]
        order_id = int(call_data[2])

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )
        if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_payment':
            if action == 'confirm':
                response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_confirm')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_confirm')

                seller_id = db_functions.get_field_info_by_response_id(response_id, 'seller')
                response_info = db_functions.get_response_info_by_response_id(response_id)

                bot.send_message(chat_id=chat_id,
                                text=text.RESPONSE_MARKED_PAID,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

                try:
                    bot.send_message(chat_id=seller_id,
                                    text=text.response_paid(*response_info),
                                    parse_mode='Markdown',
                                    reply_markup=keyboards.view_order_keyboard(order_id),
                                    )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось оповестить ({seller_id}) об оплате по отклику ({response_id}). {ex}')
                
                threading.Thread(daemon=True, target=functions.payment_to_inspect_by_admins, args=(order_id, response_id,)).start()

            elif action == 'reenter':
                db_functions.update_field_by_order_id(order_id, 'payment_photo', None)
                db_functions.update_field(user_id, 'input', True)
                db_functions.update_field(user_id, 'input_data', f'order-payment_{order_id}')

                bot.send_message(chat_id=chat_id,
                                text=text.WAITING_PAYMENT,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        else:
            bot.send_message(chat_id=seller_id,
                             text=text.RESPONSE_OUTDATED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
    
    elif query == 'payment-inspect':
        action = call_data[1]
        order_id = int(call_data[2])

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )

        if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_confirm':
            response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
            name = db_functions.get_field_info_by_order_id(order_id, 'name')
            buyer_id = db_functions.get_field_info_by_order_id(order_id, 'buyer')
            seller_id = db_functions.get_field_info_by_order_id(order_id, 'seller')

            if action == 'confirm':
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_buy')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_buy')
                
                bot.send_message(chat_id=chat_id,
                             text=text.PAYMENT_CONFIRMED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
                
                try:
                    bot.send_message(chat_id=buyer_id,
                                     text=text.payment_verified_buyer(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id, 'others'),
                                     parse_mode='Markdown',
                                     )
                except:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось оповестить покупателя ({buyer_id}) о подтверждении оплаты. {ex}')
                
                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.payment_verified_seller(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось оповестить продавца ({seller_id}) о подтверждении оплаты. {ex}')

            elif action == 'cancel':
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_buy')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_buy')

                bot.send_message(chat_id=chat_id,
                             text=text.PAYMENT_DECLINED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
                
                try:
                    bot.send_message(chat_id=buyer_id,
                                     text=text.payment_declined_buyer(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id, 'others'),
                                     parse_mode='Markdown',
                                     )
                except:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось оповестить покупателя ({buyer_id}) об отклонении подтверждения платежа. {ex}')
                
                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.payment_declined_seller(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось оповестить продавца ({seller_id}) об отклонении подтверждения платежа. {ex}')

        else:
            bot.send_message(chat_id=chat_id,
                             text=text.PAYMENT_OUTDATED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

    elif query == 'pay':
        order_id = int(call_data[1])

        if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_payment':
            response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
            response_info = db_functions.get_response_info_by_response_id(response_id)

            seller_id = db_functions.get_field_info_by_response_id(response_id, 'seller')

            name = response_info[1]
            price = response_info[2]
            delivery = response_info[3]
            comment = response_info[4]
            seller_username = db_functions.get_field_info(seller_id, 'username')

            bot.send_message(chat_id=chat_id,
                                text=text.seller_chosen(order_id, seller_username, name, price, delivery, comment),
                                reply_markup=keyboards.order_paid(order_id),
                                parse_mode='Markdown',
                                )
        else:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass

            bot.send_message(chat_id=chat_id,
                             text=text.RESPONSE_OUTDATED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

    elif query == 'received':
        order_id = int(call_data[1])
        name = db_functions.get_field_info_by_order_id(order_id, 'name')

        bot.send_message(chat_id=chat_id,
                         text=text.received_confirm(order_id, name),
                         reply_markup=keyboards.received_confirm_keyboard(order_id),
                         parse_mode='Markdown',
                         disable_notification=True,
                         )
    
    elif query == 'bought':
        response_id = int(call_data[1])
        order_id = int(call_data[2])
        page = int(call_data[3])

        name = db_functions.get_field_info_by_order_id(order_id, 'name')

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text.bought_confirm(order_id, name),
                              parse_mode='Markdown',
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.bought_confirm_keyboard(order_id, response_id, page),
                                      )
    
    elif query == 'sended':
        response_id = int(call_data[1])
        order_id = int(call_data[2])
        page = int(call_data[3])

        name = db_functions.get_field_info_by_order_id(order_id, 'name')

        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=text.sended_confirm(order_id, name),
                              parse_mode='Markdown',
                              )
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboards.sended_confirm_keyboard(order_id, response_id, page),
                                      )

    elif query == 'confirmation':
        subject = call_data[1]
        order_id = int(call_data[2])
        response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')

        if subject == 'received':
            if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_delivery':
                db_functions.update_field_by_order_id(order_id, 'status', 'done')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_transfer')
                
                order_info = db_functions.get_order_info_by_order_id(order_id)
                name = order_info[3]
                photo_id = order_info[4]

                reply_text = text.STATUS_UPDATED + text.order_info(order_id, *order_info)

                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=reply_text,
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
                
                seller_id = db_functions.get_field_info_by_order_id(order_id, 'seller')

                try:
                    bot.send_message(chat_id=seller_id,
                                     text=text.received_product(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {seller_id} о получении товара по заявке {order_id}. {ex}')

                threading.Thread(daemon=True, target=functions.to_transfer_by_admins, args=(order_id, response_id,)).start()

            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.CANT_CONFIRM_OUTDATED_DATA,
                                      parse_mode='Markdown',
                                      )

        elif subject == 'bought':
            if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_buy':
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_departure')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_departure')

                response_info = db_functions.get_response_info_by_response_id(response_id)
                name = response_info[1]

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.response_info(*response_info),
                                      parse_mode='Markdown',
                                      )
                
                buyer_id = db_functions.get_field_info_by_order_id(order_id, 'buyer')

                try:
                    bot.send_message(chat_id=buyer_id,
                                     text=text.bought_product(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id, 'others'),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {buyer_id} о покупке товара по заявке {order_id}. {ex}')

            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.STATUS_UPDATED + text.CANT_CONFIRM_OUTDATED_DATA,
                                      parse_mode='Markdown',
                                      )

        elif subject == 'sended':
            if db_functions.get_field_info_by_order_id(order_id, 'status') == 'waiting_departure':
                db_functions.update_field_by_order_id(order_id, 'status', 'waiting_delivery')
                db_functions.update_field_by_response_id(response_id, 'status', 'waiting_delivery')

                response_info = db_functions.get_response_info_by_response_id(response_id)
                name = response_info[1]
                buyer_id = db_functions.get_field_info_by_order_id(order_id, 'buyer')

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.STATUS_UPDATED + text.response_info(*response_info),
                                      parse_mode='Markdown',
                                      )
                                      
                try:
                    bot.send_message(chat_id=buyer_id,
                                     text=text.sended_product(order_id, name),
                                     reply_markup=keyboards.view_order_response_keyboard(order_id, response_id, 'others'),
                                     parse_mode='Markdown',
                                     )
                except Exception as ex:
                    logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {buyer_id} об отправке товара по заявке {order_id}. {ex}')

            else:
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text=text.CANT_CONFIRM_OUTDATED_DATA,
                                      parse_mode='Markdown',
                                      )

    elif query == 'transfer':
        order_id = int(call_data[1])
        response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')

        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=telebot.types.InlineKeyboardMarkup(),
                                      )

        if db_functions.get_field_info_by_response_id(response_id, 'status') == 'waiting_transfer':
            db_functions.update_field_by_response_id(response_id, 'status', 'done')
            db_functions.update_field(user_id, 'input', True)
            db_functions.update_field(user_id, 'input_data', f'transfer_{order_id}')

            bot.send_message(chat_id=chat_id,
                             text=text.SEND_CHECK,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

        else:
            bot.send_message(chat_id=chat_id,
                             text=text.TRANSFER_ALREADY,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with type text."""

    user_id = message.from_user.id
    chat_id = message.chat.id
    message_info = message.text
    
    input_info = db_functions.get_input_status(user_id)

    # пользователь в режиме ввода информации
    if input_info[0] and message_info not in config.REPLY_BUTTONS:
        input_data = input_info[1]

        # вводит информацию о своей роли
        if input_data == 'role':
            role = message_info.lower()

            # информация о роли является допустимой
            if role in config.ROLES:
                db_functions.update_field(user_id, 'role', config.ROLES[role])

                # пользователь еще не зарегистрирован
                if not db_functions.get_field_info(user_id, 'checked_in'):
                    # для покупателя
                    if config.ROLES[role] == 'buyer':
                        db_functions.update_field(user_id, 'input_data', 'name')
                        name = db_functions.get_field_info(user_id, 'name')

                        # если имя в профиле заполнено
                        if name:
                            bot.send_message(chat_id=chat_id,
                                             text=text.confirm_name(name),
                                             reply_markup=keyboards.confirm_data_keyboard('name'),
                                             parse_mode='Markdown',
                                             disable_notification=True,
                                             )

                        # если имя в профиле не заполнено
                        else:
                            bot.send_message(chat_id=chat_id,
                                             text=text.ASK_NAME,
                                             parse_mode='Markdown',
                                             disable_notification=True,
                                             )

                    elif config.ROLES[role] == 'seller':
                        db_functions.update_field(user_id, 'input_data', 'settings')

                        bot.send_message(chat_id=chat_id,
                                            text=text.WHOLE_WORLD,
                                            reply_markup=keyboards.settings_keyboard(),
                                            parse_mode='Markdown',
                                            disable_notification=True,
                                            )


                else:
                    if config.ROLES[role] == 'seller' and not db_functions.get_field_info(user_id, 'country_verified'):
                        db_functions.update_field(user_id, 'input_data', 'country')

                        bot.send_message(chat_id=chat_id,
                                    text=text.ASK_COUNTRY_SELLER,
                                    reply_markup=keyboards.request_country_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )

                    else:
                        db_functions.update_field(user_id, 'input_data', None)
                        db_functions.update_field(user_id, 'input', False)

                        user_info = db_functions.get_users_all_info(user_id)
                        reply = text.confirm_profile(*utils.parse_user_info(user_info))

                        role = db_functions.get_field_info(user_id, 'role')

                        bot.send_message(chat_id=chat_id,
                                        text=reply,
                                        reply_markup=keyboards.change_profile_keyboard(role),
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )

            # недопустимая информация о роли
            else:
                bot.send_message(chat_id=chat_id,
                                 text=text.ROLE_WRONG_INPUT,
                                 reply_markup=keyboards.role_keyboard(),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )

        elif input_data == 'name':
            db_functions.update_field(user_id, 'name', message_info)

            if not db_functions.get_field_info(user_id, 'checked_in'): 
                db_functions.update_field(user_id, 'input_data', 'family_name')
                family_name = db_functions.get_field_info(user_id, 'family_name')

                # если фамилия в профиле заполнена
                if family_name:
                    bot.send_message(chat_id=chat_id,
                                        text=text.confirm_family_name(family_name),
                                        reply_markup=keyboards.confirm_data_keyboard('family-name'),
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )

                # если фамилия в профиле не заполнена
                else:
                    bot.send_message(chat_id=chat_id,
                                        text=text.ASK_FAMILY_NAME,
                                        parse_mode='Markdown',
                                        disable_notification=True,
                                        )
            
            else:
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif input_data == 'family_name':
            db_functions.update_field(user_id, 'family_name', message_info)

            if not db_functions.get_field_info(user_id, 'checked_in'):
                db_functions.update_field(user_id, 'input_data', 'phone')

                bot.send_message(chat_id=chat_id,
                                    text=text.ASK_PHONE,
                                    reply_markup=keyboards.request_phone_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
            
            else:
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif input_data == 'phone':
            db_functions.update_field(user_id, 'phone', message_info)

            if not db_functions.get_field_info(user_id, 'checked_in'):
                db_functions.update_field(user_id, 'input_data', 'email')

                bot.send_message(chat_id=chat_id,
                                text=text.ASK_EMAIL,
                                reply_markup=telebot.types.ReplyKeyboardRemove(),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

            else:
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif input_data == 'email':
            db_functions.update_field(user_id, 'email', message_info)

            if not db_functions.get_field_info(user_id, 'checked_in'):
                db_functions.update_field(user_id, 'input_data', 'country')

                role = db_functions.get_field_info(user_id, 'role')

                if role == 'buyer':
                    bot.send_message(chat_id=chat_id,
                                    text=text.ASK_COUNTRY_BUYER,
                                    reply_markup=keyboards.countries_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )
                
                elif role == 'seller':
                    bot.send_message(chat_id=chat_id,
                                    text=text.ASK_COUNTRY_SELLER,
                                    reply_markup=keyboards.request_country_keyboard(),
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )

            else:
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

        elif input_data == 'country':
            if db_functions.get_field_info(user_id, 'role') == 'buyer':
                message_info = message_info.lower()

                db_functions.update_field(user_id, 'country', message_info)
                db_functions.update_field(user_id, 'input_data', None)
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'checked_in', True)

                user_info = db_functions.get_users_all_info(user_id)
                reply = text.confirm_profile(*utils.parse_user_info(user_info))

                role = db_functions.get_field_info(user_id, 'role')

                bot.send_message(chat_id=chat_id,
                                 text=reply,
                                 reply_markup=keyboards.change_profile_keyboard(role),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )

            else:
                bot.send_message(chat_id=chat_id,
                                 text=text.WRONG_COUNTRY_METHOD,
                                 reply_markup=keyboards.request_country_keyboard(),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )

        elif input_data == 'address':
            addresses = eval(db_functions.get_field_info(user_id, 'addresses'))
            addresses.append(message_info)
            db_functions.update_field(user_id, 'addresses', str(addresses))
            db_functions.update_order_field(user_id, 'address', message_info)

            bot.send_message(chat_id=chat_id,
                             text=text.confirm_address(message_info),
                             parse_mode='Markdown',
                             reply_markup=keyboards.confirm_address_keyboard(),
                             disable_notification=True,
                             )

        elif input_data == 'order_name':
            db_functions.update_order_field(user_id, 'name', message_info)
            order_status = db_functions.get_order_field_info(user_id, 'status')
            
            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_photo')
                
                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_PHOTO,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=text.confirm_order(*order_info),
                               reply_markup=keyboards.change_order_keyboard(),
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
        
        elif input_data == 'order_comment':
            db_functions.update_order_field(user_id, 'comment', message_info)
            order_status = db_functions.get_order_field_info(user_id, 'status')
            
            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_country')

                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_COUNTRY,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=text.confirm_order(*order_info),
                               reply_markup=keyboards.change_order_keyboard(),
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
        
        elif input_data == 'order_country':
            db_functions.update_order_field(user_id, 'country', message_info.lower())
            order_status = db_functions.get_order_field_info(user_id, 'status')
            
            if order_status == 'creating':
                db_functions.update_field(user_id, 'input_data', 'order_link')
                
                bot.send_message(chat_id=chat_id,
                                text=text.PRODUCT_LINK,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
            
            elif order_status == 'created':
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)
                
                order_info = db_functions.get_order_info(user_id)
                photo_id = order_info[2]

                bot.send_photo(chat_id=chat_id,
                               photo=photo_id,
                               caption=text.confirm_order(*order_info),
                               reply_markup=keyboards.change_order_keyboard(),
                               parse_mode='Markdown',
                               disable_notification=True,
                               )
        
        elif input_data == 'order_link':
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_order_field(user_id, 'link', message_info)
            db_functions.update_order_field(user_id, 'status', 'created')

            order_info = db_functions.get_order_info(user_id)
            photo_id = order_info[2]

            bot.send_photo(chat_id=chat_id,
                           photo=photo_id,
                           caption=text.confirm_order(*order_info),
                           reply_markup=keyboards.change_order_keyboard(),
                           parse_mode='Markdown',
                           disable_notification=True,
                           )

        elif 'reason' in input_data:
            order_id = int(input_data.split('_')[-1])

            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)

            db_functions.update_field_by_order_id(order_id, 'reason', message_info)

            name = db_functions.get_field_info_by_order_id(order_id, 'name')
            buyer_id = db_functions.get_field_info_by_order_id(order_id, 'buyer')

            try:
                bot.send_message(chat_id=buyer_id,
                                 text=text.order_inspected_reject(order_id, name, message_info),
                                 reply_markup=keyboards.view_order_keyboard(order_id),
                                 parse_mode='Markdown',
                                 )
            except:
                pass
                
            bot.send_message(chat_id=chat_id,
                             text=text.REJECTED_INFORMED,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

        elif input_data == 'price':
            price = utils.validate_number(message_info)
            name = db_functions.get_response_field_info(user_id, 'name') 

            if price:
                db_functions.update_response_field(user_id, 'price', price)
                response_status = db_functions.get_response_field_info(user_id, 'status')
            
                if response_status == 'creating':
                    db_functions.update_field(user_id, 'input_data', 'delivery')

                    bot.send_message(chat_id=chat_id,
                                 text=text.ask_delivery(name, price),
                                 reply_markup=keyboards.delivery_keyboard(),
                                 parse_mode='Markdown',
                                 )

                elif response_status == 'created':
                    db_functions.update_field(user_id, 'input', False)
                    db_functions.update_field(user_id, 'input_data', None)

                    response_info = db_functions.get_response_info(user_id)
            
                    bot.send_message(chat_id=chat_id,
                                    text=text.confirm_response(*response_info),
                                    reply_markup=keyboards.change_response_keyboard(),
                                    parse_mode='Markdown',
                                    )

            else:
                bot.send_message(chat_id=chat_id,
                                 text=text.incorrect_price(name),
                                 parse_mode='Markdown',
                                 )

        elif input_data == 'response_comment':
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_response_field(user_id, 'comment', message_info)
            db_functions.update_response_field(user_id, 'status', 'created')

            response_info = db_functions.get_response_info(user_id)
            
            bot.send_message(chat_id=chat_id,
                             text=text.confirm_response(*response_info),
                             reply_markup=keyboards.change_response_keyboard(),
                             parse_mode='Markdown',
                             )

        elif input_data == 'account_card' or input_data == 'account_phone':
            if 'phone' in input_data:
                account = utils.validate_phone(message.text)
            elif 'card' in input_data:
                account = utils.validate_card(message.text)

            if account:
                db_functions.update_field(user_id, 'account', account)
                db_functions.update_field(user_id, 'input_data', 'account')

                payment_form = db_functions.get_field_info(user_id, 'payment_form')
                bank = db_functions.get_field_info(user_id, 'bank')

                bot.send_message(chat_id=chat_id,
                                 text=text.confirm_bank_account(payment_form, bank, account),
                                 reply_markup=keyboards.confirm_account_keyboard(),
                                 parse_mode='Markdown',
                                 )

            else:
                bot.send_message(chat_id=chat_id,
                                 text=text.WRONG_ACCOUNT_FORMAT,
                                 parse_mode='Markdown',
                                 )

    else:

        if message_info == '🗂 Профиль':
            user_info = db_functions.get_users_all_info(user_id)
            reply = text.confirm_profile(*utils.parse_user_info(user_info))

            role = db_functions.get_field_info(user_id, 'role')

            bot.send_message(chat_id=chat_id,
                                text=reply,
                                reply_markup=keyboards.change_profile_keyboard(role, False),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif message_info == '🛒 Мои заявки':
            orders = db_functions.select_user_orders(user_id)
            status_filter = db_functions.get_field_info(user_id, 'orders_filter')

            bot.send_message(chat_id=chat_id,
                             text=text.orders_legend(status_filter),
                             reply_markup=keyboards.orders_keyboard(orders, 1, status_filter),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )
        
        elif message_info == '💵 Мои отклики':
            responses = db_functions.select_user_responses(user_id)
            status_filter = db_functions.get_field_info(user_id, 'responses_filter')

            bot.send_message(chat_id=chat_id,
                             text=text.responses_legend(status_filter),
                             reply_markup=keyboards.responses_keyboard(responses, 1, status_filter),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

        elif message_info == '❓ Помощь/справка':
            bot.send_message(chat_id=chat_id,
                             text=text.HELP,
                             reply_markup=keyboards.manager_keyboard(),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    media_group_id = message.media_group_id

    input_info = db_functions.get_input_status(user_id)

    # пользователь в режиме ввода информации
    if input_info[0]:
        input_data = input_info[1]

        if input_data == 'order_photo':
            if not media_group_id:
                photo = message.photo[-1].file_id
                db_functions.update_order_field(user_id, 'photo', photo)

                order_status = db_functions.get_order_field_info(user_id, 'status')
            
                if order_status == 'creating':
                    db_functions.update_field(user_id, 'input_data', 'order_comment')
                
                    bot.send_message(chat_id=chat_id,
                                    text=text.PRODUCT_COMMENT,
                                    parse_mode='Markdown',
                                    disable_notification=True,
                                    )

                elif order_status == 'created':
                    db_functions.update_field(user_id, 'input', False)
                    db_functions.update_field(user_id, 'input_data', None)
                    
                    order_info = db_functions.get_order_info(user_id)
                    photo_id = order_info[2]

                    bot.send_photo(chat_id=chat_id,
                                photo=photo_id,
                                caption=text.confirm_order(*order_info),
                                reply_markup=keyboards.change_order_keyboard(),
                                parse_mode='Markdown',
                                disable_notification=True,
                                )

            else:
                bot.send_message(chat_id=chat_id,
                                text=text.NO_MEDIA_GROUP,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif 'order-payment' in input_data:
            order_id = int(input_data.split('_')[-1])
            if not media_group_id:
                photo = message.photo[-1].file_id

                db_functions.update_field_by_order_id(order_id, 'payment_photo', photo)
                db_functions.update_field(user_id, 'input', False)
                db_functions.update_field(user_id, 'input_data', None)

                bot.send_photo(chat_id=chat_id,
                               photo=photo,
                               caption=text.SEND_PAYMENT_CONFIRMATION,
                               reply_markup=keyboards.payment_photo_confirmation_keyboard(order_id),
                               parse_mode='Markdown',
                               )

            else:
                bot.send_message(chat_id=chat_id,
                                text=text.NO_MEDIA_GROUP,
                                parse_mode='Markdown',
                                disable_notification=True,
                                )
        
        elif 'transfer' in input_data:
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'input_data', None)

            photo = message.photo[-1].file_id
            order_id = int(input_data.split('_')[-1])
            response_id = db_functions.get_field_info_by_order_id(order_id, 'response_id')
            name = db_functions.get_field_info_by_order_id(order_id, 'name')
            seller_id = db_functions.get_field_info_by_order_id(order_id, 'seller')

            try:
                bot.send_photo(chat_id=seller_id,
                               photo=photo,
                               caption=text.transferred(order_id, name),
                               reply_markup=keyboards.view_order_response_keyboard(order_id, response_id),
                               parse_mode='Markdown',
                               )

            except Exception as ex:
                logging.error(f'{inspect.currentframe().f_code.co_name}: Не удалось отправить уведомление пользователю {seller_id} о получении оплаты за заявку {order_id}. {ex}')

    else:
        bot.send_message(chat_id=chat_id,
                         text=text.NO_INPUT,
                         parse_mode='Markdown',
                         disable_notification=True,
                         )


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone = message.contact.phone_number
    contact_id = message.contact.user_id
    user_id = message.from_user.id
    chat_id = message.chat.id

    input_info = db_functions.get_input_status(user_id)

    if input_info[0] and input_info[1] == 'phone':
        
        db_functions.update_field(user_id, 'phone', phone)

        if user_id == contact_id:
            db_functions.update_field(user_id, 'phone_verified', True)

        if not db_functions.get_field_info(user_id, 'checked_in'):
            db_functions.update_field(user_id, 'input_data', 'email')
            bot.send_message(chat_id=chat_id,
                            text=text.ASK_EMAIL,
                            reply_markup=telebot.types.ReplyKeyboardRemove(),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )
        
        else:
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_field(user_id, 'input', False)

            user_info = db_functions.get_users_all_info(user_id)
            reply = text.confirm_profile(*utils.parse_user_info(user_info))

            role = db_functions.get_field_info(user_id, 'role')

            bot.send_message(chat_id=chat_id,
                            text=reply,
                            reply_markup=keyboards.change_profile_keyboard(role),
                            parse_mode='Markdown',
                            disable_notification=True,
                            )


@bot.message_handler(content_types=['location'])
def handle_contact(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    input_info = db_functions.get_input_status(user_id)

    if input_info[0] and input_info[1] == 'country':
        try:
            location = requests.get(utils.url_loc(message.location.latitude, message.location.longitude))
            country = location.json().get('address').get('country').lower()
        except:
            country = None
            bot.send_message(chat_id=chat_id,
                             text=text.LOCATION_ERROR,
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

        if country:
            db_functions.update_field(user_id, 'country', country)
            db_functions.update_field(user_id, 'country_verified', True)
            db_functions.update_field(user_id, 'input_data', None)
            db_functions.update_field(user_id, 'input', False)
            db_functions.update_field(user_id, 'checked_in', True)

            user_info = db_functions.get_users_all_info(user_id)
            reply = text.confirm_profile(*utils.parse_user_info(user_info))

            bot.send_message(chat_id=chat_id,
                                 text=text.found_location(country),
                                 reply_markup=telebot.types.ReplyKeyboardRemove(),
                                 parse_mode='Markdown',
                                 disable_notification=True,
                                 )

            role = db_functions.get_field_info(user_id, 'role')

            bot.send_message(chat_id=chat_id,
                             text=reply,
                             reply_markup=keyboards.change_profile_keyboard(role),
                             parse_mode='Markdown',
                             disable_notification=True,
                             )

        
if __name__ == '__main__':
    bot.polling(timeout=80)
    # while True:
    #     try:
    #         bot.polling()
    #     except:
    #         pass