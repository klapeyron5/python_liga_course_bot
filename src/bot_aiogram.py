import os
import logging
from src.utils import get_message
from hw_tests.utils import run as run_tests
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

    pb = PythonBot(bot_conf)
    pb.run()


class PythonBot:
    def __init__(self, bot_conf: dict):
        self.bot = Bot(token=bot_conf['token'])
        self.dp = Dispatcher(self.bot)

    def run(self) -> None:
        self.dp.register_message_handler(self.file_handler, content_types=types.ContentType.DOCUMENT)
        self.dp.register_message_handler(self.start, commands=['start', 'help'])
        executor.start_polling(self.dp, skip_updates=True)

    async def file_handler(self, message: types.Message):
        assert message.content_type == 'document'
        dest = os.path.join('./tmp', message.document.file_name)
        await message.document.download(destination_file=dest)
        logging.info(f"Записан файл {dest}")

        task = os.path.splitext(message.document.file_name)[0]
        res, log = run_tests(task, 'tmp')
        logging.info(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")

        await message.answer(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")

    async def start(self, message: types.Message) -> None:
        user_id = message.from_user.id
        msg = get_message('welcome') + '\n\n'
        await message.reply(msg)
