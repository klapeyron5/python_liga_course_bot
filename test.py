from src import test

def task_1(a=None,b=None,c=None,d=None):
    # print('1')
    text = input('Tip')
    print(text)
    # return 934

def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]
    assert stdin+'\n' == stdout


# кейсы первой задачи
cases = [
    'НУ Я НА ТОЧКЕ, А ВЫ ГДЕ?',
     # 'kek, я застрял в текстурах...',
     # 'ребята, gg, bb!',
]


test.run_test_cases(task_1, [
    {
        test.INPUT_stdin: 'stdin text',
        test.TEST_FUNC: test_func,
    }
])