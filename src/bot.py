import logging
import os.path

from src.utils import get_message, verify_valid, get_user_info_ad, get_full_name, get_code
from src.db_worker import DB_Worker
from configparser import ConfigParser
from telegram.update import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.callbackcontext import CallbackContext
import importlib
from multiprocessing import Pool


logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class PythonBot:

    def __init__(self, config: ConfigParser, db_worker: DB_Worker) -> None:
        logging.info('Инициализация PythonBot.')
        self.config = config
        self.bot_conf = config._sections['bot']
        self.db_worker = db_worker
        self.updater = Updater(token=self.bot_conf['token'], use_context=True)
        self.dispatcher = self.updater.dispatcher


    def run(self) -> None:
        # добавить все команды. Мб циклом?
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('register', self.register))
        self.dispatcher.add_handler(CommandHandler('set_group', self.set_group))
        self.dispatcher.add_handler(CommandHandler('status', self.status))
        self.dispatcher.add_handler(CommandHandler('my_info', self.my_info))
        self.dispatcher.add_handler(CommandHandler('get', self.get))
        self.dispatcher.add_handler(CommandHandler('verify', self.verify))
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        self.dispatcher.add_handler(MessageHandler(Filters.document, self.file_handler))
        self.updater.start_polling()
        logging.info('Готов к работе.')
        self.pool = Pool(1)


    def file_handler(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        fname = update.message['document']['file_name']
        fid = update.message['document']['file_id']
        logging.info(f'Получен файл {fname}; пользователь: {chat_id}')
        context.bot.send_message(chat_id=chat_id, text=f'Проверяю ДЗ')

        package = 'tmp'
        with open(f"./{package}/{fname}", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)

        task = os.path.splitext(fname)[0]
        # test_module = 'hw_tests_prod.test_' + task
        tasks = [task,]

        def f(task):
            m = importlib.import_module(f'{package}.test_' + task)
            res, log = m.run(package)
            return res, log

        args = [list((x,)) for x in tasks]
        out = self.pool.starmap(f, args)[0]
        res, log = out

        # test_module = 'hw_tests_prod.test_'+os.path.splitext(fname)[0]
        # testing_module = importlib.import_module(test_module)
        # res, log = testing_module.run('tmp')

        # logging.info(f'Отправка файла; пользователь: {chat_id}')
        context.bot.send_message(chat_id=chat_id, text=f'Проверил ДЗ. Результат: {res}. Логи: {log}')


    def is_registered(self, update: Update, context: CallbackContext) -> bool:
        chat_id = update.effective_chat.id
        result = False
        if not self.db_worker.user_exists(chat_id):
            context.bot.send_message(chat_id=chat_id, text='Вы не зарегистрированы! Воспользуйтесь командой /register.')
        elif not self.db_worker.get_group_id(chat_id):
            context.bot.send_message(chat_id=chat_id, text='У вас не установлена группа! Воспользуйтесь командой /set_group.')
        else:
            result = True
        return result


    def start(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде start; пользователь: {chat_id}')

        message = get_message('welcome') + '\n\n'
        if self.db_worker.user_exists(chat_id):
            message += f'Приветствую, {self.db_worker.get_name(chat_id)}.'
        else:
            message += get_message('suggest_register')
        context.bot.send_message(chat_id=chat_id, text=message)


    def help(self, update: Update, context: CallbackContext) -> None:
        context.bot.send_message(parse_mode='HTML', chat_id=update.effective_chat.id, text=get_message('help'))


    def register(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде register; пользователь: {chat_id}')

        user_input = update.message.text[10:]
        if not user_input:
            message = 'Вы не указали логин. Попробуйте снова.'
        elif not self.db_worker.user_exists(chat_id):
            ad_login = user_input.split(' ')[0]
            code = get_code(user_input)
            result = verify_valid(ad_login, code)
            if result['status']:
                self.db_worker.register_user(chat_id, ad_login, result['full_name'])
            message = result['message']
        else:
            message = 'Вы уже зарегистрированы'
        
        context.bot.send_message(chat_id=chat_id, text=message)


    def set_group(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде set_group; пользователь: {chat_id}')

        group_id = int(update.message.text.split(' ')[-1])
        if self.db_worker.user_exists(chat_id) and group_id:
            result = self.db_worker.set_group_id(chat_id, group_id)
            if result['status'] == 'success':
                message = 'Ваш новый номер группы: ' + str(group_id)
            else:
                message = 'Не могу сменить ваш номер группы. Пожалуйста, обратитесь к администратору.'
        elif not group_id:
            message = 'Вы не указали номер группы. Попробуйте снова.'
        else:
            message = 'Вы не зарегистрированы! Воспользуйтесь командой /register.'
        context.bot.send_message(chat_id=chat_id, text=message)


    def my_info(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде my_info; пользователь: {chat_id}')
        if not self.is_registered(update, context):
            return

        info = self.db_worker.select_user_info(chat_id)[0]
        message = f'Ваш логин: {info[0]}\nВаша группа: {info[1]}'
        tests = set([el[0] for el in self.db_worker.get_tests()])
        for test in tests:
            message += '\n' + self.get_test_status(chat_id, test)
        context.bot.send_message(chat_id=chat_id, text=message)


    def get(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде get; пользователь: {chat_id}')
        if not self.is_registered(update, context):
            return

        test, task = update.message.text.split(' ')[1].split('-')
        if self.db_worker.is_completed(chat_id, test, task):
            message = f'Вы уже выполнили задачу №{task} Практики №{test}.'
        else:
            message = f'Практика №{test}\n'
            message += self.db_worker.get_question(test, task)
        context.bot.send_message(chat_id=chat_id, text=message)


    def verify(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде verify; пользователь: {chat_id}')
        if not self.is_registered(update, context):
            return
        # print('verify0')
        # print(update.message)
        # try:
        #     context.bot.get_file(update.message.document).download()
        #     with open("file.doc", 'wb') as f:
        #         context.bot.get_file(update.message.document).download(out=f)
        #     print('FILE')
        # except Exception as e:
        #     print(str(e))
        # print('verify1')
        split = update.message.text.split(' ')
        test, task = split[1].split('-')
        answer = (' ').join(split[2:])
        if self.db_worker.is_completed(chat_id, test, task):
            message = f'Вы уже выполнили задачу №{task} Практики №{test}.'
        else:
            correct = self.db_worker.get_correct(test, task)
            result = self.db_worker.check_answer(answer, correct)
            if result['mark']:
                message = f'Ответ на задачу {test}-{task} верный!'
                self.db_worker.add_student_progress(chat_id, test, task)
            elif 'ORA' in result['status']:
                message = f"Неверный запрос. Ошибка {result['status']}"
            else:
                message = f'Ответ неверный.'
        context.bot.send_message(chat_id=chat_id, text='verify_message')


    def get_test_status(self, chat_id: str, test: str) -> str:
        tasks = self.db_worker.get_tasks(chat_id, test)
        questions = self.db_worker.get_questions(test)
        completed = set([task[0] for task in tasks])
        uncompleted = set(range(1, len(questions)+1)).difference(completed)
        if len(uncompleted) == len(questions):
            message = f'Вы ещё не приступали к Практике №{test}.'
        elif uncompleted:
            message = f'Практика №{test}, номера незавершенных задач: {str(uncompleted)[1:-1]}'
        else:
            message = f'Вы прошли Практику №{test}!'
        return message


    def status(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        logging.info(f'Обращение к команде verify; пользователь: {chat_id}')
        if not self.is_registered(update, context):
            return

        test = update.message.text.split(' ')[1]
        if self.db_worker.test_available(test):
            message = self.get_test_status(chat_id, test)
        else:
            message = f'Практика №{test} не найдена.'
        context.bot.send_message(chat_id=chat_id, text=message)