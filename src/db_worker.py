import logging
import cx_Oracle
from configparser import ConfigParser
from typing import Union, List, Tuple, Dict


logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class DB_Worker:

    def __init__(self, config: ConfigParser) -> None:
        logging.info('Инициализация DB_Worker.')
        self.config = config
        self.dbname = self.config._sections['db']['dbname']
        self.user = self.config._sections['db']['user']
        self.pwd = self.config._sections['db']['pwd']
        self.host = self.config._sections['db']['host']
        self.port = self.config._sections['db']['port']
        self.check_connection()


    def connect_to_db(self) -> cx_Oracle.Connection:
        dsn = cx_Oracle.makedsn(self.host, self.port, self.dbname)
        return cx_Oracle.connect(user=self.user, password=self.pwd, dsn=dsn, encoding="UTF-8", nencoding="UTF-8")


    def check_connection(self) -> None:
        logging.info('Проверяем соединение с базой...')
        try:
            con = self.connect_to_db()
            logging.info(f'Соединение с базой {self.dbname} установлено.')
        except Exception as e:
            logging.critical(f'Не могу установить соединение с базой {self.dbname}.')
            logging.critical(str(e))
            exit()


    def select_user_info(self, chat_id: int) -> Tuple:
        query = 'SELECT * FROM SQL_BOT_USERS WHERE chat_id = ' + str(chat_id)
        return self.query_select(query)['data']


    def user_exists(self, chat_id: int) -> bool:
        return bool(self.select_user_info(chat_id))


    def get_name(self, chat_id: int) -> str:
        return self.select_user_info(chat_id)[0][0]


    def get_group_id(self, chat_id: int) -> str:
        return self.select_user_info(chat_id)[0][1]


    def query_select(self, query: str) -> Dict[str, str]:
        # кидает селект в базу
        logging.info(f'Обращение к базе (SELECT): {query}')
        result = {'status': '', 'data': ''}
        con = self.connect_to_db()
        cur = con.cursor()
        try:
            result['data'] = cur.execute(query).fetchall()
            result['status'] = 'success'
        except Exception as e:
            str_e = str(e)
            logging.warning(str_e)
            result['status'] = str_e
        return result


    def query_insert(self, query: str) -> Dict[str, str]:
        # закидывает данные в базу
        logging.info(f'Обращение к базе (INSERT): {query}')
        result = {'status': '', 'data': ''}
        con = self.connect_to_db()
        cur = con.cursor()
        try:
            cur.execute(query)
            con.commit()
            result['status'] = 'success'
        except Exception as e:
            logging.warning(str(e))
        return result


    def register_user(self, chat_id: str, ad_login: str, username: str) -> Dict[str, str]:
        # инсертит в базу значения
        logging.info(f"Регистрируем пользователя {username}, chat_id: {chat_id}")
        query = f"""INSERT INTO SQL_BOT_USERS (NAME, GROUP_ID, CHAT_ID, LOGIN)
        VALUES ('{username}', '', '{chat_id}', '{ad_login}')"""
        return self.query_insert(query)


    def set_group_id(self, chat_id: str, group_id: int) -> Dict[str, str]:
        result = False
        query =  f"""UPDATE SQL_BOT_USERS SET group_id = {group_id} WHERE chat_id = '{chat_id}'"""
        return self.query_insert(query)


    def is_completed(self, chat_id: str, test: str, task: str) -> bool:
        query = f"""SELECT * FROM SQL_BOT_PROGRESS WHERE test = {int(test)} AND task = {int(task)} AND chat_id = {int(chat_id)}"""
        return bool(self.query_select(query)['data'])


    def get_question(self, test: str, task: str) -> Tuple:
        query = f"""SELECT question FROM SQL_BOT_ASSIGNMENTS WHERE test = {int(test)} AND task = {int(task)}"""
        return self.query_select(query)['data'][0][0]


    def get_correct(self, test: str, task: str) -> Tuple:
        query = f"""SELECT answer FROM SQL_BOT_ASSIGNMENTS WHERE test = {int(test)} AND task = {int(task)}"""
        return self.query_select(query)['data'][0][0]


    def get_tasks(self, chat_id: str, test: str) -> Tuple:
        query = f"SELECT task FROM SQL_BOT_PROGRESS WHERE chat_id = '{chat_id}' AND test = {test}"
        return self.query_select(query)['data']


    def get_questions(self, test: str) -> Tuple:
        query = f"""SELECT question FROM SQL_BOT_ASSIGNMENTS WHERE test = {int(test)}"""
        return self.query_select(query)['data']


    def get_tests(self) -> Tuple:
        query = f"""SELECT test FROM SQL_BOT_ASSIGNMENTS"""
        return self.query_select(query)['data']


    def test_available(self, test: str) -> bool:
        tests = set([el[0] for el in self.get_tests()])
        return True if int(test) in tests else False


    def check_answer(self, answer: str, correct: str) -> Dict[str, str]:
        query = f'{correct} MINUS {answer}'
        result = self.query_select(query)
        result['mark'] = False
        if not result['data'] and result['status'] == 'success':
            result['mark'] = True
        return result


    def add_student_progress(self, chat_id: str, test: str, task: str) -> Dict[str, str]:
        name = self.get_name(chat_id)
        group_id = self.get_group_id(chat_id)
        query = f"""
        INSERT INTO SQL_BOT_PROGRESS (name, group_id, chat_id, test, task)
        VALUES ('{name}', {group_id}, {chat_id}, {test}, {task})
        """
        return self.query_insert(query)