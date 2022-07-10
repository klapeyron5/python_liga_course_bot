from unittest import mock
import io

INPUT_stdin = 'stdin'
INPUT_arg = 'arg'
INPUT_kwarg = 'kwarg'

TEST_FUNC = 'test_func'
OUTPUT_stdout = 'stdout'
OUTPUT_returned = 'returned'

CASE_KEYS = {INPUT_stdin, INPUT_arg, INPUT_kwarg, TEST_FUNC}


def run_test_cases(func, cases):
    tests_passed = []
    tests_failed = []
    for i, case in enumerate(cases):
        extkeys = set(case.keys()) - CASE_KEYS
        assert extkeys == set(), f"Extra keys in test case: {extkeys}"

        stdin = case.get(INPUT_stdin, None)
        if isinstance(stdin, str):
            mock.builtins.input = lambda *args, **kwargs: stdin
        else:
            it = iter(stdin)
            mock.builtins.input = lambda *args, **kwargs: it.__next__()

        # кладем в переменную output то, что выводится программкой в stdout
        with mock.patch('sys.stdout', new=io.StringIO()) as output:
            output_return = func(*case.get(INPUT_arg, []), **case.get(INPUT_kwarg, dict()))
        output_stdout = output.getvalue()
        try:
            case[TEST_FUNC](**{**case, **{OUTPUT_stdout: output_stdout, OUTPUT_returned: output_return}})
            tests_passed.append(i)
        except Exception as e:
            print(e)
            tests_failed.append(i)
    return {
        'passed': tests_passed,
        'failed': tests_failed,
    }
