from unittest import mock
import io

INPUT_stdin = 'stdin'  # str or list of inputs for consecutive input()
INPUT_args = 'args'
INPUT_kwargs = 'kwargs'

TEST_FUNC = 'test_func'
OUTPUT_stdout = 'stdout'
OUTPUT_returned = 'returned'

CASE_KEYS = {INPUT_stdin, INPUT_args, INPUT_kwargs, TEST_FUNC}


def run_test_cases(func, cases):
    """
    func: func to test
    cases: list of test cases
    """
    tests_passed = []
    tests_failed = []
    for i, case in enumerate(cases):
        extkeys = set(case.keys()) - CASE_KEYS
        assert extkeys == set(), f"Extra keys in test case: {extkeys}"
        if INPUT_stdin not in case:
            case[INPUT_stdin] = None
        if INPUT_args not in case:
            case[INPUT_args] = []
        if INPUT_kwargs not in case:
            case[INPUT_kwargs] = {}

        stdin = case[INPUT_stdin]
        if isinstance(stdin, str):
            mock.builtins.input = lambda *args, **kwargs: stdin
        else:
            it = iter(stdin)
            mock.builtins.input = lambda *args, **kwargs: it.__next__()

        # кладем в переменную output то, что выводится программкой в stdout
        with mock.patch('sys.stdout', new=io.StringIO()) as output:
            output_return = func(*case[INPUT_args], **case[INPUT_kwargs])
        output_stdout = output.getvalue()
        try:
            # testing outputs here
            case[TEST_FUNC](**{**case, **{OUTPUT_stdout: output_stdout, OUTPUT_returned: output_return}})
            tests_passed.append(i)
        except Exception as e:
            print(e)
            tests_failed.append(i)
    return {
        'passed': tests_passed,
        'failed': tests_failed,
    }
