import telebot
from telebot import types
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


TOKEN = '6016077533:AAGIjfjJreRJ30Tq7U-UF6ZACp34C_tv2U4'

# создаем бота с токеном
bot = telebot.TeleBot(TOKEN)

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group = Column(String)


Session = sessionmaker(bind=engine)


def add_user(name, group):
    session = Session()
    user = User(name=name, group=group)
    session.add(user)
    session.commit()
    session.close()


def get_user(name):
    session = Session()
    user = session.query(User).filter_by(name=name).first()
    session.close()
    return user


@bot.message_handler(commands=['register'])
def register(message):
    bot.send_message(message.chat.id, "Для регистрации введите свое имя:")
    bot.register_next_step_handler(message, ask_group)


def ask_group(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите номер группы:")
    bot.register_next_step_handler(message, save_user, name)


def save_user(message, name):
    group = message.text
    add_user(name, group)
    bot.send_message(message.chat.id, "Вы успешно зарегистрировались!")


# Подключение к базе данных
DATABASE_URL = 'postgres://user:password@host:port/database'
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

TOKEN = 'your_token_here'
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Розклад на сьогодня')
    item2 = types.KeyboardButton('Розклад на завтра')
    item3 = types.KeyboardButton('Розклад на цю неділю')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привіт, {0.first_name}! Я бот-розклад.'.format(message.from_user),
                     reply_markup=markup)


# Обработчик сообщений с текстом

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Розклад на сьогодня':
            # Запрос данных из базы данных
            cur = conn.cursor()
            cur.execute("SELECT * FROM schedule WHERE day = 'today'")
            rows = cur.fetchall()

            # Формирование сообщения с рассписанием
            schedule = ''
            for row in rows:
                schedule += f"{row[1]} - {row[2]}\n"
            bot.send_message(
                message.chat.id, 'Розклад на сьогодня:\n' + schedule)

        elif message.text == 'Розклад на завтра':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Розклад на завтра')
            item2 = types.KeyboardButton('Розклад на цю неділю')
            back = types.KeyboardButton('Повернутися назад')
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id, '6 марта пойдешь на пары, спи', reply_markup=markup)

        elif message.text == 'Розклад на цю неділю':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('о парах')
            item2 = types.KeyboardButton('я на пары')
            back = types.KeyboardButton('Повернутися назад')
            markup.add(item1, item2, back)
            bot.send_message(
                message.chat.id, 'Розклад на цю неділю', reply_markup=markup)

        elif message.text == 'Повернутися назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Розклад на сьогодня')
            item2 = types.KeyboardButton('Розклад на завтра')
            item3 = types.KeyboardButton('Розклад на цю неділю')
            markup.add(item1, item2,)


bot.polling(non_stop=True)
