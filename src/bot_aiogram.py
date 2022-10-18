import os
import logging

import pandas as pd

from src.utils import get_message, get_code, get_full_name, verify_valid
from src.db_worker import DB_Worker
from hw_tests_prod.utils import run as run_tests, _check_task_name_format
from configparser import ConfigParser
from aiogram import Bot, Dispatcher, executor, types

import cx_Oracle
import sys

try:
    if sys.platform.startswith("darwin"):
        lib_dir = os.path.join(os.environ.get("HOME"), "Downloads", "instantclient_19_8")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("win32"):
        lib_dir = r"C:\oracle\instantclient_21_6"
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Whoops!")
    print(err);
    sys.exit(1);


def parse_config(config_file: str) -> ConfigParser:
    logging.info(f'Loading config file {config_file}')
    config = ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config


def check_assignments(dbw):
    tests = os.listdir(os.path.join(os.path.dirname(__file__), '../', 'hw_tests_prod'))
    tests_names = []
    for t in tests:
        if t[:5] == 'test_':
            tname, ext = os.path.splitext(t[5:])
            assert ext == '.py'
            try:
                _check_task_name_format(tname)
                tests_names.append(tname)
            except Exception:
                pass
    with dbw.connect_to_db() as c:
        df = pd.read_sql('select TASK from PYTHON_BOT_ASSIGNMENTS', c)
    assert set(tests_names) == set(df.TASK.values)


def run(config_file):
    with open('log.txt', 'w') as f:
        pass
    # os.remove('log.txt')
    logging.basicConfig(filename='log.txt',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    config = parse_config(config_file=config_file)
    db_worker = DB_Worker(config)
    check_assignments(db_worker)
    bot_conf = config._sections['bot']
    logging.info('Bot initializing')

    pb = PythonBot(bot_conf, db_worker)
    pb.run()


def reply_exception(func):
    async def wrapped(self, message: types.Message, **kwargs):
        try:
            await func(self, message, **kwargs)
        except Exception as e:
            await message.reply(str(e))
    return wrapped


class PythonBot:
    def __init__(self, bot_conf: dict, db_worker: DB_Worker):
        self.bot = Bot(token=bot_conf['token'])
        self.dp = Dispatcher(self.bot)
        self.db_worker = db_worker

    def run(self) -> None:
        self.dp.register_message_handler(self.start, commands=['start', 'help'])
        self.dp.register_message_handler(self.register, commands=['register'])
        self.dp.register_message_handler(self.set_group, commands=['set_group'])
        self.dp.register_message_handler(self.my_info, commands=['my_info'])
        self.dp.register_message_handler(self.file_handler, content_types=types.ContentType.DOCUMENT)
        executor.start_polling(self.dp, skip_updates=True)

    @reply_exception
    async def file_handler(self, message: types.Message, **kwargs):
        chat_id = message.from_id
        assert message.content_type == 'document'
        dir_path = os.path.join('tmp', str(chat_id))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        dest = os.path.join(dir_path, message.document.file_name)
        await message.document.download(destination_file=dest)

        task = os.path.splitext(message.document.file_name)[0]
        res, log = run_tests(task, dir_path.replace(os.sep, '.'))

        if self.db_worker.is_completed(chat_id, task):
            await message.answer(f'Вы уже выполнили задачу {task}. Результаты проверки присланного варианта: {res}. Лог: {log}')
        else:
            await message.answer(f"Протестировано задание {task}. Результат: {res}. Лог: {log}")
            if res == 1:
                insert_res = self.db_worker.add_student_progress(chat_id, task=task)
                if not insert_res['status']:
                    await message.answer(insert_res['log'])

    async def start(self, message: types.Message) -> None:
        # chat_id = message.from_user.id
        msg = get_message('help') + '\n\n'
        await message.reply(msg, parse_mode='HTML')

    @reply_exception
    async def register(self, message: types.Message, **kwargs) -> None:
        chat_id = message.from_id
        user_input = message.text[10:]

        if not user_input:
            txt = 'Вы не указали логин. Попробуйте снова.'
        elif not self.db_worker.user_exists(chat_id):
            split = user_input.split(' ')
            ad_login = split[0]
            ad_fio = ' '.join(split[1:])
            assert len(ad_fio) > 0, 'Укажите ФИО'
            # code = get_code(user_input)
            # result = verify_valid(ad_login, code)
            # if result['status']:
            # self.db_worker.register_user(chat_id, ad_login, result['full_name'])
            self.db_worker.register_user(chat_id, ad_login, ad_fio)
            # txt = result['message']
            txt = f"Зарегистрирован пользователь логин: {ad_login}, ФИО: {ad_fio}"
        else:
            txt = 'Вы уже зарегистрированы'
        await message.reply(txt)

    @reply_exception
    async def set_group(self, message: types.Message, **kwargs) -> None:
        chat_id = message.from_id
        group_id = int(message.text.split(' ')[-1])
        if self.db_worker.user_exists(chat_id) and group_id:
            result = self.db_worker.set_group_id(chat_id, group_id)
            if result['status'] == 'success':
                txt = 'Ваш новый номер группы: ' + str(group_id)
            else:
                txt = 'Не могу сменить ваш номер группы. Пожалуйста, обратитесь к администратору.'
        elif not group_id:
            txt = 'Вы не указали номер группы. Попробуйте снова.'
        else:
            txt = 'Вы не зарегистрированы! Воспользуйтесь командой /register.'
        await message.reply(txt)

    async def is_registered(self, message) -> bool:
        chat_id = message.from_id
        result = False
        if not self.db_worker.user_exists(chat_id):
            await message.reply(text='Вы не зарегистрированы! Воспользуйтесь командой /register.')
        elif not self.db_worker.get_group_id(chat_id):
            await message.reply(text='У вас не установлена группа! Воспользуйтесь командой /set_group.')
        else:
            result = True
        return result

    @reply_exception
    async def my_info(self, message: types.Message, **kwargs) -> None:
        chat_id = message.from_id
        if not await self.is_registered(message):
            return
        info = self.db_worker.select_user_info(chat_id)[0]
        txt = f'Ваш логин: {info[-1]}\nВаша группа: {info[1]}\nВаше ФИО: {info[0]}'
        all_tasks = set([el[0] for el in self.db_worker.get_all_tasks()])
        user_tasks = set([el[0] for el in self.db_worker.get_user_tasks(chat_id)])
        assert set(user_tasks) - set(all_tasks) == set()
        uncompleted = set(all_tasks) - set(user_tasks)
        df = pd.DataFrame({'task': list(user_tasks)+list(uncompleted), 'completed': [1]*len(user_tasks)+[0]*len(uncompleted)})
        df = df.sort_values('task')
        txt += '\n\nСтатус выполнения заданий:'
        txt += '\ndone\t\ttask'
        for r in df.values:
            txt += '\n' + str(r[1]) + '\t\t' + str(r[0])
        await message.reply(txt, parse_mode='HTML')
