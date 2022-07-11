from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    # main content of tests
    assert stdin+'\n' == stdout, f'stdout "{stdout}" does not equals stdin "{stdin}"'


cases = [
    {
        test.INPUT_stdin: x,
        test.TEST_FUNC: test_func,
    } for x in ['НУ Я НА ТОЧКЕ, А ВЫ ГДЕ?','kek, я застрял в текстурах...','ребята, gg, bb!']
]


def run(package_name):
    return test.run('L04_HW_task1', cases, package_name=package_name)
