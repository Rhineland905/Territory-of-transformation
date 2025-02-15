import mysql.connector
import telebot
import re

my_bot = telebot.TeleBot('5116218178:AAHThqvo_5BpxJv8L_kpgrM_a7LQPZQEfI4')

config_tg = {
    'user': 'root',
    'password': '8012',
    'host': 'localhost',
    'database': 'test'
}

conn_tg = mysql.connector.connect(**config_tg)

markup = telebot.types.InlineKeyboardMarkup()
button = telebot.types.InlineKeyboardButton('Реєстрація', callback_data='register')
markup.add(button)
def is_valid_name(text):
    pattern = r'^[А-Яа-яЇїІіЄєҐґ]{2,}$'
    return bool(re.match(pattern, text))
def firts_name(message):
    id = message.from_user.id
    text = message.text
    if is_valid_name(text):
        with conn_tg.cursor() as curs:
            curs.execute("UPDATE user SET first_name=%s WHERE user_id=%s", (text, id))
            conn_tg.commit()
            curs.execute(f'SELECT * FROM  user WHERE user_id=%s', (id,))
            user_data = curs.fetchall()
        if not user_data[0][3]:
            my_bot.send_message(message.chat.id, "Введіть фамілію")
            my_bot.register_next_step_handler(message, last_name)
    else:
        my_bot.send_message(message.chat.id, "Ви ввели неправильне ім'я")
        my_bot.register_next_step_handler(message, firts_name)

def last_name(message):
    id = message.from_user.id
    text = message.text
    if is_valid_name(text):
        with conn_tg.cursor() as curs:
            curs.execute("UPDATE user SET last_name=%s WHERE user_id=%s", (text, id))
            conn_tg.commit()
            my_bot.send_message(message.chat.id, "Ви успішно зареєструвалися")
    else:
        my_bot.send_message(message.chat.id, "Ви ввели неправильне прізвище")
        my_bot.register_next_step_handler(message, last_name)

@my_bot.message_handler(commands=['start'])
def start(message):
    my_bot.send_message(message.chat.id, f'<text>', reply_markup=markup)

@my_bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "register":
        id = call.from_user.id
        with conn_tg.cursor() as curs:
            curs.execute(f'SELECT * FROM  user WHERE user_id=%s', (id,))
            user_data = curs.fetchall()
        if not user_data:
            with conn_tg.cursor() as curs:
                curs.execute("INSERT INTO user(user_id) VALUES (%s)",(id,))
                conn_tg.commit()
            my_bot.send_message(call.message.chat.id, "Введіть ім'я")
            my_bot.register_next_step_handler(call.message, firts_name)





my_bot.polling()


