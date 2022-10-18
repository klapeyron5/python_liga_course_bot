from hw_tests_prod import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    args = kwargs[test.INPUT_args]

    returned = kwargs[test.OUTPUT_returned]
    stdout = kwargs[test.OUTPUT_stdout]

    # тестируем логику модуля как функцию
    def main(x1: str, y1: str, x2: str, y2: str):
        d_x = int(x2) - int(x1)
        d_y = int(y2) - int(y1)
        if d_x != 0:
            return d_y / d_x
        return 'undefined'

    assert returned == main(*args)


cases = [{test.INPUT_args: x, test.TEST_FUNC: test_func} for x in [
    [19, 3, 20, 3],
    [-7, 2, -7, 4],
    [3, 3, 7, 9]
]]


def run(package_name):
    return test._run('L06_HW_task2', cases, func_name='main', package_name=package_name)
