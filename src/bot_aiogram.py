import os
import logging
from hw_tests.utils import run
from configparser import ConfigParser
from aiogram import Bot, Dispatcher, executor, types


def parse_config(config_file: str) -> ConfigParser:
    logging.info(f'Loading config file {config_file}')
    config = ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config


def run(config_file):
    os.remove('log.txt')
    logging.basicConfig(filename='log.txt',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    config = parse_config(config_file=config_file)
    bot_conf = config._sections['bot']
    logging.info('Bot initializing')
    bot = Bot(token=bot_conf['token'])
    dp = Dispatcher(bot)

    @dp.message_handler(content_types=types.ContentType.DOCUMENT)
    async def file_handler(message: types.Message):
        assert message.content_type == 'document'
        dest = os.path.join('./tmp', message.document.file_name)
        await message.document.download(destination_file=dest)
        logging.info(f"Записан файл {dest}")

        task = os.path.splitext(message.document.file_name)[0]
        res, log = run(task, 'tmp')
        logging.info(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")

        await message.answer(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")

    executor.start_polling(dp, skip_updates=True)
