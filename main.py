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


async def send_typing(stop_event, message):
    print("печать")
    ranges = 60
    while not stop_event.is_set():
        print("печать луп" + str(ranges))
        await bot.send_chat_action(message.chat.id, 'typing')
        await asyncio.sleep(1)  # Подождать 1 секунду перед отправкой следующего действия печати
        await asyncio.sleep(5)  # Подождать 5 секунд перед отправкой следующего набора действий печати
        ranges -= 1
        if ranges < 1:
            stop_event.set()

    print("Залуп закончился")

async def send_message_to_GPT(message, chat_history):
     print("Запрос в GPT")
     stop_event = asyncio.Event()
     task = asyncio.create_task(send_typing(stop_event, message))
     response = await g4f.ChatCompletion.create_async(
         model=g4f.models.default,
        messages=chat_history,
       provider=g4f.Provider.Bing,
     )
     stop_event.set()
     return response


#
# async def main(message, chat_history):
#     print("зашел в маин")
#     send_message_task = asyncio.create_task(send_message_to_GPT(message, chat_history))
#     send_typing_task = asyncio.create_task(send_typing(await send_message_task, message))
#     await send_message_task
#     await send_typing_task
#     return send_typing_task.result()





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
    user_message = "Найди ближайшие футбольные матчи и выведи их в виде списка. В списке должны быть только названия команд и дата время его проведенрия и больше ничего. В тексте убери форматирование. Важно Не пиши список источников."
    user_id = message.from_user.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_message})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]

    try:

        print("UserName @" + message.from_user.username)
        print("Message " + message.text)
        await message.answer("Происходит сбор информации...")
        #response = await main(message, chat_history)
        response = await send_message_to_GPT(message, chat_history)
        chat_gpt_response = response

    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
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
    user_message = "1.Представь что ты спортивный аналитик и ты должен проанализировать результаты поиска в интернете 2. Ты должен сделать подробные выводы по полученной информации 3.Ты не должен выводить в ответе мой запрос 4.Ты должен вывести источники которые использовал в самом конце письма 5.Ты должен убрать все форматирование текста" + message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_message})
    conversation_history[user_id] = trim_history(conversation_history[user_id])
    chat_history = conversation_history[user_id]

    try:
        print("Запрос в GPT")
        print("UserName @" + message.from_user.username)
        print("Message " + message.text)

        await message.answer("Происходит сбор информации...")
        await bot.send_chat_action(message.chat.id, 'typing')
        response = await send_message_to_GPT(message, chat_history)
        chat_gpt_response = response


    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)

        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    stop_event = asyncio.Event()
    stop_event.set()
    await message.answer(chat_gpt_response)
    await message.answer("Заходи в MOSTBET и выйграй 25 000р бонусов!")
    await message.answer("https://xo9d7f7z5v8r8bsmst.com/Vigs")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
