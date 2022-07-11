from hw_tests import utils as test
import inspect
import re


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    # main content of tests
    funcs = inspect.getmembers(rtrn, inspect.isfunction)
    funcs_names = [x[0] for x in funcs]
    funcs = [x[1] for x in funcs]
    excess_funcs = set(funcs_names) - {'get_x','get_y','squared_error','linear_regression',}
    assert excess_funcs == set(), excess_funcs
    for f in funcs:
        assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None
    assert stdout[:4] == 'SE: '
    se = int(stdout[4:])
    assert (1+1*stdin[0] - stdin[1])**2 == se


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [1, 3],
    [10, 2],
]]
results = test.run_test_cases(test.get_module_test('L04_HW_project'), cases=cases)
print(results)
