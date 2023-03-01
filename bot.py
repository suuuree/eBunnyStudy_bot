import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# настройка логирования
logging.basicConfig(level=logging.INFO)

# инициализация бота и диспетчера
bot = Bot(token='6016077533:AAEUkewTRaFvoLzFo05cgQwhXX36iWYjst0')
dp = Dispatcher(bot)

# Клавиатура для выбора действий после регистрации
registered_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
today_button = KeyboardButton(text="Показать расписание на сегодня")
tomorrow_button = KeyboardButton(text="Показать расписание на завтра")
registered_keyboard.add(today_button, tomorrow_button)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Создаем кнопки для регистрации
    registration_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="Зарегистрироваться")
    registration_keyboard.add(button)

    # Отправляем сообщение с кнопками регистрации
    await message.answer("Привет! Я бот. Хотите зарегистрироваться?", reply_markup=registration_keyboard)


# Обработчик нажатия на кнопку "Зарегистрироваться"
@dp.message_handler(text="Зарегистрироваться")
async def register_user(message: types.Message, first_name_last_name=None):
    # Спрашиваем у пользователя имя и фамилию
    await message.answer("Как Вас зовут? (имя и фамилия)")
    message = await bot.await_next_message(chat_id=message.chat.id)


    # Спрашиваем у пользователя курс
    await message.answer("На каком Вы курсе? (число)")
    course = await bot.await_for_message(chat_id=message.chat.id)

    # Спрашиваем у пользователя номер группы
    await message.answer("Какой у Вас номер группы?")
    group_number = await bot.await_for_message(chat_id=message.chat.id)

    # Сохраняем данные пользователя в базу данных
    user_id = message.from_user.id
    user_data = {
        'user_id': user_id,
        'first_name': first_name_last_name.text.split()[0],
        'last_name': first_name_last_name.text.split()[1],
        'course': course.text,
        'group_number': group_number.text,
    }
    # Здесь должен быть код для сохранения данных пользователя в базу данных
    print(user_data)

    # Отправляем сообщение о успешной регистрации с использованием имени и фамилии пользователя
    await message.answer(f"Вы успешно зарегистрированы, {user_data['first_name']} {user_data['last_name']}!", reply_markup=registered_keyboard)


# Обработчик нажатия на кнопку "Показать расписание на сегодня"
@dp.message_handler(text="Показать расписание на сегодня")
async def show_schedule_today(message: types.Message):
    # Здесь должен быть код для показа расписания на сегодня

    # Отправляем расписание
    await message.answer("Расписание на сегодня")

# Обработчик нажатия на кнопку "Показать расписание на завтра"
@dp.message_handler(text="Показать расписание на завтра")
async def show_schedule_tomorrow(message: types.Message):
    # Здесь должен быть код для показа расписания на завтра

    # Отправляем расписание
    await message.answer("Расписание на завтра")

# запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()


