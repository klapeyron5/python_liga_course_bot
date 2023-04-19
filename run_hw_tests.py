from hw_tests_prod.utils import run
import pandas as pd
from src.db_worker import DB_Worker
from configparser import ConfigParser
import cx_Oracle
import sys, os
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
config_file = './data/config.ini'
def parse_config(config_file: str) -> ConfigParser:
    config = ConfigParser()
    config.read(config_file, encoding='utf-8')
    return config
config = parse_config(config_file=config_file)
# dbw = DB_Worker(config)

package = 'hw_examples'

# with dbw.connect_to_db() as c:
#     df = pd.read_sql('select TASK from PYTHON_BOT_ASSIGNMENTS', c)
# tasks = df.TASK.values
tasks = [
    'L04_HW_project',
    'L04_HW_task1',
    'L04_HW_task2',
    'L04_HW_task3',
    'L05_HW_project',
    'L06_HW_project',
    'L06_HW_task1',
    'L06_HW_task2',
    'L07_HW_project',
    'L08_HW_project',
    'L09_HW_project',
    'L10_HW_project',
    'L11_HW_project',
]

outs = [run(t, package) for t in tasks]

passed = 0
for task, out in zip(tasks, outs):
    passed += out[0]
print(f'Успешно протестировано {passed} ДЗ из {len(tasks)}')
for task, out in zip(tasks, outs):
    if not out[0]:
        print(f'Провалено задание {task}: {out[1]}')
