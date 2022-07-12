import sys
import importlib
from unittest import mock
import io

INPUT_stdin = 'stdin'  # str or list of inputs for consecutive input()
INPUT_args = 'args'
INPUT_kwargs = 'kwargs'

TEST_FUNC = 'test_func'
OUTPUT_stdout = 'stdout'
OUTPUT_returned = 'returned'
OUTPUT_module = 'module'

CASE_KEYS = {INPUT_stdin, INPUT_args, INPUT_kwargs, TEST_FUNC}


def run_test_cases(func, cases):
    """
    func: func to test
    cases: list of test cases
    """
    tests_passed = []
    tests_failed = []
    for i, case in enumerate(cases):
        extkeys = set(case.keys()) - CASE_KEYS
        assert extkeys == set(), f"Extra keys in test case: {extkeys}"
        if INPUT_stdin not in case:
            case[INPUT_stdin] = None
        if INPUT_args not in case:
            case[INPUT_args] = []
        if INPUT_kwargs not in case:
            case[INPUT_kwargs] = {}

        stdin = case[INPUT_stdin]
        if isinstance(stdin, str):
            mock.builtins.input = lambda *args, **kwargs: stdin
        elif stdin is not None:
            it = iter(stdin)
            mock.builtins.input = lambda *args, **kwargs: it.__next__()

        # кладем в переменную output то, что выводится программкой в stdout
        with mock.patch('sys.stdout', new=io.StringIO()) as output:
            output_return = func(*case[INPUT_args], **case[INPUT_kwargs])
        output_stdout = output.getvalue()
        try:
            # testing outputs here
            case[TEST_FUNC](**{**case, **{OUTPUT_stdout: output_stdout, OUTPUT_returned: output_return}})
            tests_passed.append(i)
        except Exception as e:
            print(e)
            tests_failed.append(i)
    return {
        'passed': tests_passed,
        'failed': tests_failed,
    }


def _reimport_module(task_name, package):
    global module
    task_name = package+'.'+task_name
    if package not in sys.modules:
        module = importlib.import_module(task_name)
    else:
        importlib.reload(module)
    return module


def get_module_test(module_name, package='hw_examples'):
    if not _check_task_name_format(module_name):
        raise Exception(f'Неверный формат имени тестируемого модуля: {module_name}')
    def body():
        return _reimport_module(module_name, package)
    return body


def run(module_name, cases, func_name=None, test_module=None, package_name='hw_examples'):
    """
    module_name: имя модуля, который тестируем (имя файла с решением задания)
    func_name: функция, которую тестируем. Если None, значит вся логика выполняется в global scope модуля (подходит для первых ДЗ)
    cases: кейсы для тестирования func_name или module_name. Список словарей с ключами INPUT_stdin, INPUT_args, INPUT_kwargs, TEST_FUNC.
           INPUT-ключи не обязательны, TEST_FUNC - обязателен.
           INPUT_stdin может быть как str (если в программе один вызов input()) так и [str] (список строк на вход последовательным запросам input())
    test_module: функция, которая тестирует модуль целиком (оформление, имена функций, документация, используемые либы и т.д.)
    package_name: имя пакета, в котором лежит решенное задание (hw_examples для примеров верных заданий, tmp - для полученных от бота)
    """
    out_result = 1
    out_log = "Тесты пройдены"

    if not _check_task_name_format(module_name):
        raise Exception(f'Wrong format of tested module name: {module_name}')

    if func_name is None:
        tested_func = lambda: _reimport_module(module_name, package_name)
    else:
        tested_module = _reimport_module(module_name, package_name)
        tested_func = getattr(tested_module, func_name)
        try:
            test_module(tested_module)
        except:
            out_result = 0
            out_log = "Проблема с оформлением кода (имена функций, документация, использование библиотек)"
            return out_result, out_log

    results = run_test_cases(tested_func, cases=cases)
    if len(results['failed']) != 0:
        out_result = 0
        out_log = f"Провалено {len(results['failed'])} тестов из {len(results['passed'])+len(results['failed'])}"
        return out_result, out_log

    return out_result, out_log

def _check_task_name_format(tn):
    """
    Examples of right formats:
    L04_HW_project
    L11_HW_task1
    L09_HW_task10
    """
    try:
        assert tn[0] == 'L'
        L = int(tn[1:3])
        assert L >= 1
        assert tn[3:7] == '_HW_'
        c0 = tn[7:] == 'project'
        try:
            task_number = int(tn[11:])
        except:
            task_number = 0
        c1 = tn[7:11] == 'task' and task_number >= 1 and len(str(task_number)) == len(tn[11:])
        assert c0 or c1
        return 1
    except:
        return 0
