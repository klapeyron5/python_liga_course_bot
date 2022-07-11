from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

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


def run(package_name):
    return test.run('L04_HW_task3', cases, package_name=package_name)
