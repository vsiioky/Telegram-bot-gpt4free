import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота с использованием переменных окружения для токена
API_TOKEN = os.getenv('6858952505:AAF30YotG9XNoprDN5VfceGAsaE9eSvZgi0')  # Добавьте ваш токен здесь как fallback
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения истории разговоров
conversation_history = {}

def trim_history(user_id, max_length=4096):
    """Функция для обрезки истории разговора."""
    history = conversation_history.get(user_id, [])
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("Доброго времени суток")
    await message.answer("Я ваш персональный помошник для анализа предстоящих спортивных событий")
    await message.answer("Введите названия команд (Название команды1 - Название команды2)")

@dp.message_handler(commands=['near'])
async def near_command(message: types.Message):
    """Обработчик команды /near."""
    user_message = "Найди ближайшие футбольные матчи и выведи их в виде списка. В тексте убери форматирование. Не пиши приветствие. В тексте убери все знаки *. Не пиши того, что ты не сделал по моей инструкции"
    user_id = message.from_user.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": user_message})
    trim_history(user_id)
    # Здесь должен быть ваш код для запроса данных, например, через g4f
    await message.answer("Информация по вашему запросу собирается...")

@dp.message_handler(commands=['clear'])
async def clear_command(message: types.Message):
    """Обработчик команды /clear."""
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("История диалога очищена.")

@dp.message_handler()
async def text_message_handler(message: types.Message):
    """Обработчик текстовых сообщений."""
    user_id = message.from_user.id
    user_message = "1.Представь, что ты спортивный аналитик и ты должен проанализировать результаты поиска в интернете 2. Ты должен сделать подробные выводы по полученной информации 3.Ты не должен выводить в ответе мой запрос 4.Ты должен вывести источники, которые использовал 5.Ты не должен отвечать текстом, который содержит форматирование " + message.text
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": user_message})
    trim_history(user_id)
    # Здесь должен быть ваш код для обработки сообщения, например, запрос через g4f
    await message.answer("Ваш запрос обрабатывается...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
