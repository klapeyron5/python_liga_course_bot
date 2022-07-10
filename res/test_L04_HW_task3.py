import sys
from src import test
from importlib import reload


def run_test():
    if 'HW_examples' not in sys.modules:
        from HW_examples import L04_HW_task3
    else:
        global L04_HW_task3
        reload(L04_HW_task3)


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
results = test.run_test_cases(run_test, cases=cases)
print(results)
