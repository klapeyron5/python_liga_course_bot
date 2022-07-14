from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]  # здесь возвращается ссылка на модуль L06_HW_task2, т.к. global scope модуля и есть тестируемая программа

    # тестируем логику модуля как функцию
    def task_2(x1: str, y1: str, x2: str, y2: str):
        d_x = int(x2) - int(x1)
        d_y = int(y2) - int(y1)
        if d_x != 0:
            return d_y / d_x
        return 'undefined'

    s = task_2(stdin[0], stdin[1], stdin[2], stdin[3])
    assert s == stdout.rstrip('\n')


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [19, 3, 20, 3],
    [-7, 2, -7, 4],
    [3, 3, 7, 9]
]]


def run(package_name):
    return test.run('L06_HW_task2', cases, package_name=package_name)
