from hw_tests import utils as test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]

    # main content of tests
    assert stdin+'#spudik' == stdout, f'stdout "{stdout}" does not equals stdin "{stdin}"'


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    'with my BOYS, eating pizza on rooftops!',
    'sheesh, have you seen this goblin?',
    'okey, guys, the last one...',
]]


def run(package_name):
    return test.run('L04_HW_task2', cases, package_name=package_name)
