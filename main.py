import mysql.connector
import telebot
import re

my_bot = telebot.TeleBot('5116218178:AAHThqvo_5BpxJv8L_kpgrM_a7LQPZQEfI4')

config_tg = {
    'user': 'u4756_HKNCHJXNZp',
    'password': '7LY6raurZ+w2RDLJW9FlrZ+P',
    'host': '84.46.246.159',
    'database': 's4756_Telegram_bot'
}

conn_tg = mysql.connector.connect(**config_tg)

@my_bot.message_handler(commands=['start'])
def start(message):
    try:

        with conn_tg.cursor() as curs:
            curs.execute('SELECT * FROM users WHERE user_id=%s',(str(message.from_user.id),))
            user = curs.fetchone()
        if user is None:
            with conn_tg.cursor() as curs:
                curs.execute("INSERT INTO users (first_name, last_name,username, user_id, chat_id) VALUES (%s, %s, %s, %s, %s)", (str(message.from_user.first_name), str(message.from_user.last_name),str(message.from_user.username), str(message.from_user.id), str(message.chat.id)))
                conn_tg.commit()
        my_bot.send_message(message.chat.id, f'Привіт. Я Phenix bot я можу:')
    except:
        my_bot.reply_to(message, 'Виникла помилка. Спробуйте ще раз та перевірти вірно ви написали команду')


my_bot.polling()