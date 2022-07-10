from src import test
from .utils import get_module_test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]
    assert rtrn is None, f'Returned value is not None {rtrn}'

    # main content of tests
    s = f"{stdin[0]} + {stdin[1]} = {stdin[0] + stdin[1]}\n{stdin[0]} - {stdin[1]} = {stdin[0] - stdin[1]}\n\
{stdin[0]} * {stdin[1]} = {stdin[0] * stdin[1]}\n{stdin[0]} // {stdin[1]} = {stdin[0] // stdin[1]}\n\
{stdin[0]} % {stdin[1]} = {stdin[0] % stdin[1]}\n"
    assert s == stdout

cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [1, 2],
    [1234, 1234],
    [-18, 3],
]]
results = test.run_test_cases(get_module_test('L04_HW_task3'), cases=cases)
print(results)
