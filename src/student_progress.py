import pandas as pd
from typing import List, Dict
from collections import defaultdict
from src.db_worker import DB_Worker


ignore = ['Nikita Vlasov', 'Василий Б. Здоров', 'Пахан', 'lblynskiy']


def create_df_users(db_worker: DB_Worker) -> pd.DataFrame:
    result = db_worker.query_select("SELECT * FROM SQL_BOT_USERS")
    return pd.DataFrame(result['data'], columns=['name', 'group_id', 'chat_id', 'smth'])


def create_df_progress(db_worker: DB_Worker) -> pd.DataFrame:
    result = db_worker.query_select("SELECT * FROM SQL_BOT_PROGRESS")
    return pd.DataFrame(result['data'], columns=['name', 'chat_id', 'group_id', 'task', 'test', 'date'])


def check_exists(arg, value, all_values):
    if not value == 'all':
        for value in range(int(value[0]), int(value[-1])+1):
            if value not in all_values:
                print(f'Не найден {arg}, значение: {value}. Доступные значения: {sorted(all_values)}')
                exit()


def check_args(args: Dict, progress: pd.DataFrame, users: pd.DataFrame, tests: defaultdict) -> None:
    values = {
    'practice': list(tests.keys()), # все существующие практики
    'group': users.group_id.unique() # все существующие группы
    }
    for arg, value in args.items():
        check_exists(arg, value, values[arg])


def create_tests_length(db_worker: DB_Worker) -> Dict[int, int]:
    data = db_worker.query_select("SELECT test, task FROM SQL_BOT_ASSIGNMENTS")['data']
    result = defaultdict(lambda: set())
    for test, task in data:
        result[test].add(task)
    return result


def write_report(debtors: defaultdict, detailed: str) -> None:
    filename = 'Прогресс студентов.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('Должники: ')
        f.write(', '.join(debtors.keys()))
        f.write('\n\n')
        f.write(detailed[:-2])
    print(f'\nОтчет сохранен как "{filename}"', end='')


def create_report(args: Dict, db_worker: DB_Worker='') -> str:
    tests_length = create_tests_length(db_worker)
    dfs = {
    'progress': create_df_progress(db_worker),
    'users': create_df_users(db_worker),
    'tests': tests_length
    }

    check_args(args, **dfs)
    if args['group'] == 'all':
        args['group'] = dfs['users'].group_id.dropna().unique().astype(int)
    if args['practice'] == 'all':
        args['practice'] = sorted(list(tests_length.keys()))

    debtors = defaultdict(lambda: [])
    detailed = ''
    for group in range(args['group'][0], args['group'][-1]+1):
        detailed += '= '*6 + f'Группа: {group}' + ' ='*6
        current_group = dfs['progress'][dfs['progress'].group_id == group]
        for student in current_group.chat_id.unique():
            name = current_group[current_group.chat_id == student].iloc[0]['name']
            if name in ignore:
                continue
            detailed += f'\nСтудент: {name}'
            print(f'Смотрю группу {group}, студент: {name}', end='\r')
            student_progress = current_group[current_group.chat_id == student]
            for test in range(int(args['practice'][0]), int(args['practice'][-1])+1):
                completed = len(student_progress[student_progress.test == test].task)
                if completed == len(tests_length[test]):
                    mark = '✔'
                else:
                    mark = '☓'
                    debtors[name].append(test)
                detailed += f'\nПрактика №{test}, решено заданий: {completed}/{len(tests_length[test])} [{mark}]'
            detailed += '\n\n'

    write_report(debtors, detailed)