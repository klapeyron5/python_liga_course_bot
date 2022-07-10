from src import test
from .utils import get_module_test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    # main content of tests
    assert stdin+'\n' == stdout, f'stdout "{stdout}" does not equals stdin "{stdin}"'


results = test.run_test_cases(get_module_test('L04_HW_task1'), [
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
