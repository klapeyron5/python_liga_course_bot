import os
import logging
from typing import List, Dict, Union
from src.db_worker import DB_Worker
from src.student_progress import create_report
from src.utils import get_message, parse_config
from argparse import ArgumentParser, RawTextHelpFormatter, Namespace


logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def check_args(args: Dict, default: str) -> None:
    for arg, value in args.items():
        if value != default:
            try:
                int(value[0]), int(value[-1])
            except (ValueError, TypeError):
                print(f'Некорректно указан аргумент {arg}.')
                print('Аргументы должны быть указаны либо цифрой (1; 4), либо диапазоном (1-5; 2-4)')
                exit()


def get_args() -> Namespace:
    default = 'all' # это значение ещё используется в src/student_progress.py
    parser = ArgumentParser(description=get_message('help_form_report'), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--practice', type=str, help=get_message('help_args_practice'), nargs='?', default=default)
    parser.add_argument('--group', type=str, help=get_message('help_args_group'), nargs='?', default=default)
    args = parser.parse_args()
    check_args(vars(args), default)
    return args


if __name__ == '__main__':
    args = get_args()
    path_to_config = os.path.join('data', 'config.ini')
    db_worker = DB_Worker(parse_config(path_to_config))
    logging.info(f'Формируем отчет, группа: {str(args.group)}; практика: {str(args.practice)}')
    print('Создаю отчет.\n')
    create_report(vars(args), db_worker)