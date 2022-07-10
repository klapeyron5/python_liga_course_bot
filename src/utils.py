import os
import logging
import platform
from configparser import ConfigParser
from typing import List, Dict
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES


logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def parse_config(config_file: str) -> ConfigParser:
    logging.info(f'Загружаем конфиг {config_file}')
    config = ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config


def get_message(message_file) -> str:
    path_to_file = os.path.join('data', 'messages', f'{message_file}.txt')
    with open(path_to_file, encoding='UTF-8') as f:
        return f.read()


def read_assignment(filename: str) -> List[str]:
    filename = os.path.join('assignments', 'filename')
    with open(filename, 'r', encoding='utf-8') as f:
        split = f.read().split('\n\n')
        questions, answers = [], []
        for s in split:
            q, a = s.split('\nОтвет: ')
            questions.append(q)
            answers.append(a)
        return questions, answers


def get_insert_assignment() -> None:
    assignments = os.listdir('assignments')
    for file in assignments:
        test = file[0]
        questions, answers = read_assignment(file)
        for task, (q, a) in enumerate(zip(questions, answers)):
            query = f"""INSERT INTO SQL_BOT_ASSIGNMENTS (TEST, TASK, QUESTION, ANSWER)
VALUES ({test}, {task+1}, '{q}', '{a.replace("'", '"')}')"""
            yield query


def get_user_info_ad(ad_login: str) -> bool:
    server = Server('ldap://192.168.245.50', get_info=ALL)
    conn = Connection(server, user='phoenixit\\toolset', password='hG4A45D#De', auto_bind=True, auto_referrals=False)
    conn.search('dc=phoenixit,dc=ru', f'(&(objectclass=person)(sAMAccountName={ad_login}))', attributes=['userPrincipalName'])
    return conn.entries


def get_full_name(ad_responce: str) -> str:
    return str(ad_responce[0])[7:].split(',')[0]


def generate_code(ad_login: str) -> int:
    return sum([ord(l) for l in ad_login])


def get_code(user_input: str) -> int:
    code = 0
    try:
        code = int(user_input.split(' ')[-1])
    except ValueError:
        pass
    return code


def verify_valid(ad_login: str, code: int) -> Dict:
    """
    проверяет что пользователь есть
    сверяет его код
    если пользователь есть и код совпадает, регистрируем
    если пользователь есть, а кода нет, выдать пользователю инфу и код
    """
    result = {'status': False, 'message': '', 'code': generate_code(ad_login)}
    if ad_login and ad_login.split(' ')[0].isalpha():
        ad_responce = get_user_info_ad(ad_login)
        full_name = get_full_name(ad_responce)
    else:
        ad_responce = ''
        result['message'] = 'Пользователь не найден. Укажите ваш логин.'
    
    if ad_responce and code == result['code']:
        result['status'] = True
        result['message'] = f'Вы успешно зарегистрированы как {full_name}'
        result['full_name'] = full_name
    elif ad_responce and code:
        result['message'] = 'Неправильный код подтверждения.'
    elif not code and ad_responce:
        result['message'] += f"Ваше имя: {full_name}\nВаш код верификации: {result['code']}\n"
        result['message'] += f"Для завершения регистрации введите:\n/register {ad_login} {result['code']}"
    return result


if __name__ == '__main__':
    user_input = 'azolotarev'
    ad_login = user_input.split(' ')[0]
    code = get_code(user_input)
    result = verify_valid(ad_login, code)
    print(result['status'], result['message'])
    