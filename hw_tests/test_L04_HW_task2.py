from src import test
from .utils import get_module_test


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]
    assert rtrn is None, f'Returned value is not None {rtrn}'

    # main content of tests
    assert stdin+'#spudik' == stdout, f'stdout "{stdout}" does not equals stdin "{stdin}"'


cases = [{test.INPUT_stdin: x, test.TEST_FUNC: test_func} for x in [
    'with my BOYS, eating pizza on rooftops!',
    'sheesh, have you seen this goblin?',
    'okey, guys, the last one...',
]]


results = test.run_test_cases(get_module_test('L04_HW_task2'), cases=cases)
print(results)
