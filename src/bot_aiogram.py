import os
import logging
import importlib
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5116564871:AAFkLOYK0nNfpkb5aPyYIXmSmLUYGvFuDZA'

# Configure logging
os.remove('log.txt')
logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def f(task):
    m = importlib.import_module('hw_tests.test_'+task)
    res, log = m.run('tmp')
    return res, log

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def file_handler(message: types.Message):
    assert message.content_type == 'document'
    dest = os.path.join('./tmp', message.document.file_name)
    await message.document.download(destination_file=dest)
    logging.info(f"Записан файл {dest}")

    task = os.path.splitext(message.document.file_name)[0]
    res, log = f(task)
    logging.info(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")

    await message.answer(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")


def run():
    executor.start_polling(dp, skip_updates=True)
