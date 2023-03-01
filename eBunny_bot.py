import telebot
import mysql.connector

# Настройки подключения к базе данных
cnx = mysql.connector.connect(user='USERNAME', password='PASSWORD',
                              host='HOST', database='SQLite')

# Создание объекта бота
bot = telebot.TeleBot('6016077533:AAEUkewTRaFvoLzFo05cgQwhXX36iWYjst0')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может помочь тебе найти расписание занятий. Введи номер группы, например: /group 12345")

# Обработчик команды /group
@bot.message_handler(commands=['group'])
def handle_group(message):
    # Получение номера группы из сообщения
    group_number = message.text.split()[1]

    # Выполнение SQL-запроса
    cursor = cnx.cursor()
    query = "SELECT * FROM schedule WHERE group_number=%s"
    cursor.execute(query, (group_number,))

    # Формирование сообщения с результатами
    result_message = "Расписание для группы {}:\n\n".format(group_number)
    for result in cursor:
        result_message += "Дата: {}\n".format(result[0])
        result_message += "Время: {} - {}\n".format(result[1], result[2])
        result_message += "Преподаватель: {}\n\n".format(result[3])

    # Отправка сообщения с результатами
    bot.reply_to(message, result_message)

# Запуск бота
bot.polling()
