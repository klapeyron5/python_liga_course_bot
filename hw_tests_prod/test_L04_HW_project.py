from hw_tests_prod import utils as test
import inspect
import re


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    module = kwargs[test.OUTPUT_returned]  # здесь возвращается ссылка на модуль L04_HW_project, т.к. global scope модуля и есть тестируемая программа

    if inspect.ismodule(module):
        # тестируем код модуля
        funcs = inspect.getmembers(module, inspect.isfunction)
        funcs_names = [x[0] for x in funcs]
        funcs = [x[1] for x in funcs]
        excess_funcs = set(funcs_names) - {'get_x', 'get_y', 'squared_error', 'linear_regression', }
        assert excess_funcs == set(), excess_funcs
        for f in funcs:
            assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None

        # тестируем логику модуля как функцию
        assert stdout[:4] == 'SE: '
        se = int(stdout[4:])
        a0 = int(stdin[0])
        a1 = int(stdin[1])
        assert (1+1*a0 - a1)**2 == se
    elif isinstance(module, ValueError):
        try:
            a0 = int(stdin[0])
            a1 = int(stdin[1])
            raise Exception
        except ValueError as e:
            pass
    else:
        raise Exception


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    ['1', 3],
    [10, 2],
    ['asd',3],
]]


def run(package_name):
    return test._run('L04_HW_project', cases, package_name=package_name)
