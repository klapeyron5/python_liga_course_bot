import os
import logging
from configparser import ConfigParser
from src.bot import SQL_Bot
from src.utils import parse_config, get_insert_assignment
from src.db_worker import DB_Worker
import cx_Oracle


log_file = 'log.txt'
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def migrate_assignments_to_db(config: ConfigParser) -> None:
    # переносит все практики и задания из папки assigments в таблицу SQL_BOT_ASSIGNMENTS
    db_worker = DB_Worker(config)
    gen = get_insert_assignment()
    for query in gen:
        #db_worker.query_insert(query)
        print(query)


def start_bot(config: ConfigParser) -> None:
    # db_worker = DB_Worker(config)
    sql_bot = SQL_Bot(config, db_worker=None)
    # sql_bot = SQL_Bot(config, db_worker=None)
    sql_bot.run()
    print('Бот готов к работе и ждет сообщений.')
    print('Лог работы сохраняется в', log_file)


if __name__ == '__main__':
    print('====================')
    logging.info('\n\nНачало работы программы.')
    path_to_config = os.path.join('data', 'config-prod.ini')
    # path_to_config = os.path.join('data', 'config.ini')
    config = parse_config(path_to_config)
    start_bot(config)
    # migrate_assignments_to_db(config)