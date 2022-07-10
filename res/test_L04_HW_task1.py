import sys

from src import test
from importlib import reload

L04_HW_task1 = None


def run_test():
    if 'HW_examples' not in sys.modules: # hasattr(sys.modules['tmp'], 'L04_HW_task1')
        from HW_examples import L04_HW_task1
    else:
        global L04_HW_task1
        reload(L04_HW_task1)


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]
    assert rtrn is None, f'Returned value is not None {rtrn}'

    # main content of tests
    assert stdin+'\n' == stdout, f'stdout "{stdout}" does not equals stdin "{stdin}"'


results = test.run_test_cases(run_test, [
    {
        test.INPUT_stdin: 'НУ Я НА ТОЧКЕ, А ВЫ ГДЕ?',
        test.TEST_FUNC: test_func,
    },
    {
        test.INPUT_stdin: 'kek, я застрял в текстурах...',
        test.TEST_FUNC: test_func,
    },
    {
        test.INPUT_stdin: 'ребята, gg, bb!',
        test.TEST_FUNC: test_func,
    },
])

print(results)
