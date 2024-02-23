import logging
from aiogram import Bot, Dispatcher, types
import g4f
from aiogram.utils import executor
import asyncio

# Включите логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = '6858952505:AAF30YotG9XNoprDN5VfceGAsaE9eSvZgi0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения истории разговоров
conversation_history = {}

# Функция для обрезки истории разговора
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

async def send_message_to_GPT(message, chat_history):
    print("Запрос в GPT")
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        messages=chat_history,
        provider=g4f.Provider.Bing,
    )
    return response

async def send_typing(response, message):
    print("печать")
    while response == "":
        for i in range(5):
            await bot.send_chat_action.typing(message.chat.id)
            await asyncio.sleep(1)  # Подождать 1 секунду перед отправкой следующего действия печати
        await asyncio.sleep(5)  # Подождать 5 секунд перед отправкой следующего набора действий печати

async def main(message, chat_history):
    print("зашел в маин")
    send_message_task = asyncio.create_task(send_message_to_GPT(message, chat_history))
    send_typing_task = asyncio.create_task(send_typing(await send_message_task, message))
    await send_message_task
    await send_typing_task





@dp.message_handler(commands=['start'])
async def process_clear_command(message: types.Message):
    print("start")
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("Доброго времени суток")
    await message.answer ("Я ваш персональный помошник для анализа предстоящих спортивных событий")
    await message.answer ("введите названия команд (Название команды1 - Название команды2)")

@dp.message_handler(commands=['near'])
async def process_clear_command2(message: types.Message):
    user_message = "Найди ближайшие футбольные матчи и выведи их в виде списка. В тексте убери форматирование. Не пиши приветствие. В тексте убери все знаки *. ВЫВЕДИ ТОЛЬКО СПИСОК!"
    user_id = message.from_user.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_message})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]

    try:
        print(message.text)
        await message.answer("Происходит сбор информации...")
        print("gjgsnrf pfqnb d main")
        response = asyncio.run(main(message, chat_history))
        #response = await send_message_to_GPT(message, chat_history)
        chat_gpt_response = response

    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    await message.answer(response)
    print(response + "Near resp")
    await message.reply(response)

@dp.message_handler(commands=['clear'])
async def process_clear_command(message: types.Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("История диалога очищена.")

# Обработчик для каждого нового сообщения
@dp.message_handler()
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_message = "1.Представь что ты спортивный аналитик и ты должен проанализировать результаты поиска в интернете 2. Ты должен сделать подробные выводы по полученной информации 3.Ты не должен выводить в ответе мой запрос 4.Ты должен вывести источники которые использовал 5.Ты не должен отвечать текстом который содержит форматирование 6. НЕ ПИШИ НИЧЕГО ЧТО НЕ КАСАЕТСЯ АНАЛИТИКИ" + message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_message})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]

    try:
        print("Запрос в GPT")
        print(message.text)
        await message.answer("Происходит сбор информации...")
        print("hello typing")
        await bot.send_chat_action(message.chat.id, 'typing')

        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=g4f.Provider.Bing,
        )
        chat_gpt_response = response

    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    await message.answer(chat_gpt_response)
    await message.answer("Сыылка на контору")
    await message.answer("промокод")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
