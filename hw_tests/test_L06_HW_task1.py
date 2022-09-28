from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    args = kwargs[test.INPUT_args]

    returned = kwargs[test.OUTPUT_returned]
    stdout = kwargs[test.OUTPUT_stdout]

    def main(x: str, y: str, z: str):
        x = int(x)
        y = int(y)
        z = int(z)
        if x and y:
            return 'life detected!'
        elif x or y:
            if z:
                return 'life detected!'
            else:
                return 'nothing...'
        else:
            return 'nothing...'

    assert stdout == main(*args)


cases = [{test.INPUT_args: x, test.TEST_FUNC: test_func} for x in [
    [1, 0, 1],
    [0, 0, 1],
    [1, 1, 0]
]]


def run(package_name):
    return test._run('L06_HW_task1', cases, func_name='main', package_name=package_name)
