from hw_tests_prod import utils as test
from hw_examples import L06_HW_project
import inspect
import re


def test_module(module):
    all_vars = [x for x in inspect.getmembers(module) if not x[0].startswith('__')]
    all_vars_names = [x[0] for x in all_vars]
    excess_vars = set(all_vars_names) ^ {
        'get_int', 'get_x', 'get_y', 'error', 'squared_error', 'pipeline', 'calculate_zone', 'linear_regression',\
            'DEFAULT_b0', 'DEFAULT_b1', 'SIGMA', 'MU'}
    assert excess_vars == set()

    funcs = inspect.getmembers(module, inspect.isfunction)
    funcs_names = [x[0] for x in funcs]
    funcs = [x[1] for x in funcs]
    excess_funcs = set(funcs_names) ^ {'get_int', 'get_x', 'get_y', 'error', 'squared_error', 'linear_regression', 'pipeline', 'calculate_zone'}
    assert excess_funcs == set(), excess_funcs
    for f in funcs:
        assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None
    assert module.DEFAULT_b0 == 1
    assert module.DEFAULT_b1 == 1
    assert module.SIGMA == 1
    assert module.MU == 0

    assert module.calculate_zone(6, sigma=2, mu=1) == 'orange'

def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    if rtrn is None:
        so_se, so_ez, res = stdout.split('\n')
        assert res == ''

        assert so_se[:4] == 'SE: '
        se = int(so_se[4:])
        a0 = int(stdin[0])
        a1 = int(stdin[1])
        e = 1+1*a0 - a1
        assert e**2 == se

        assert so_ez[:12] == 'Error zone: '
        assert L06_HW_project.calculate_zone(e) == so_ez[12:]
    elif isinstance(rtrn, ValueError):
        try:
            a0 = int(stdin[0])
            a1 = int(stdin[1])
            raise Exception
        except ValueError as e:
            assert isinstance(rtrn,ValueError)
    else:
        raise Exception

    


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [1, 5],
    [1, 6],
    [1, 3],
    [10, '2'],
    ['', 13],
    [9,9],
]]


def run(package_name):
    return test._run('L06_HW_project', cases, func_name='pipeline', test_module=test_module, package_name=package_name)

