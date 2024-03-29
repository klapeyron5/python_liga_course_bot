from hw_tests_prod import utils as test
import inspect
import re


def test_module(module):
    funcs = inspect.getmembers(module, inspect.isfunction)
    funcs_names = [x[0] for x in funcs]
    funcs = [x[1] for x in funcs]
    excess_funcs = set(funcs_names) ^ {'get_int', 'get_x', 'get_y', 'squared_error', 'linear_regression', 'pipeline'}
    assert excess_funcs == set(), excess_funcs
    for f in funcs:
        assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None
    assert module.DEFAULT_b0 == 1
    assert module.DEFAULT_b1 == 1


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    if rtrn is None:
        assert stdout[:4] == 'SE: '
        se = int(stdout[4:])
        a0 = int(stdin[0])
        a1 = int(stdin[1])
        e = 1+1*a0 - a1
        assert e**2 == se
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
    [1, 3],
    [10, '2'],
    [10,'!'],
]]


def run(package_name):
    return test._run('L05_HW_project', cases, func_name='pipeline', test_module=test_module, package_name=package_name)

