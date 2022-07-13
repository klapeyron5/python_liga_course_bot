from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]  # здесь возвращается ссылка на модуль L05_HW_task1, т.к. global scope модуля и есть тестируемая программа

    # тестируем логику модуля как функцию
    def divisible_by_x(a: int, b: int):
        def divisible_by_y(c: int):
            return stdin[0] % c

        return stdin[0] % a + divisible_by_y(b)

    s = f'total remainder of divisions equals {divisible_by_x(stdin[1], stdin[2])};'
    assert s == stdout.rstrip('\n')


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [10, 2, 3],
    [21, 5, 4],
]]


def run(package_name):
    return test.run('L05_HW_task1', cases, package_name=package_name)
