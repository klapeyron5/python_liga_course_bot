from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]  # здесь возвращается ссылка на модуль L05_HW_task1, т.к. global scope модуля и есть тестируемая программа

    # тестируем логику модуля как функцию
    def task_1(n: str, x: str, y: str):
        def divisible_by_x(a: int, b: int):
            def divisible_by_y(c: int):
                return n % c

            return n % a + divisible_by_y(b)

        n, x, y = int(n), int(x), int(y)
        return f'total remainder of divisions equals {divisible_by_x(x, y)};'

    s = task_1(stdin[0], stdin[1], stdin[2])
    assert s == stdout.rstrip('\n')


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [10, 2, 3],
    [21, 5, 4],
]]


def run(package_name):
    return test._run('L05_HW_task1', cases, package_name=package_name)
