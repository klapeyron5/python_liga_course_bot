from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]  # здесь возвращается ссылка на модуль L06_HW_task1, т.к. global scope модуля и есть тестируемая программа

    # тестируем логику модуля как функцию
    def task_1(x: str, y: str, z: str):
        x, y, z = int(x), int(y), int(z)
        if x and y:
            return 'life detected!'
        elif x or y:
            if z:
                return 'life detected!'
            return 'nothing...'
        return 'nothing...'

    s = task_1(stdin[0], stdin[1], stdin[2])
    assert s == stdout.rstrip('\n')


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    [1, 0, 1],
    [0, 0, 1],
    [1, 1, 0]
]]


def run(package_name):
    return test._run('L06_HW_task1', cases, package_name=package_name)
