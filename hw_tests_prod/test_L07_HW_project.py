from hw_tests_prod import utils as test
from hw_examples import L07_HW_project
import inspect
import re


def test_module(module):
    classes = inspect.getmembers(module, inspect.isclass)
    assert len(classes)==1
    assert classes[0][0] == 'LinearRegression'
    LinearRegression = classes[0][1]
    init_code = inspect.getsource(LinearRegression.__init__)
    init_definition = init_code[:init_code.find(':')].replace('\n','').replace('\\','').replace(' ','')
    assert init_definition.startswith('def__init__(')
    assert init_definition.endswith(')')
    init_definition = init_definition[len('def__init__('):-1]
    init_kwargs = init_definition.split(',')
    assert 'b0=DEFAULT_b0' in init_kwargs
    assert 'b1=DEFAULT_b1' in init_kwargs
    methods = inspect.getmembers(LinearRegression, inspect.ismethod)
    lr = LinearRegression(3,-4)
    assert lr.predict(2) == -5
    assert lr.predict(0) == 3

    all_vars = [x for x in inspect.getmembers(module) if not x[0].startswith('__')]
    all_vars_names = [x[0] for x in all_vars]
    excess_vars = set(all_vars_names) ^ {
        'get_float', 'error', 'squared_error', 'pipeline', 'calculate_zone', \
            'LinearRegression', 'DEFAULT_b0', 'DEFAULT_b1', 'SIGMA'}
    assert excess_vars == set()
    
    funcs = inspect.getmembers(module, inspect.isfunction)
    funcs_names = [x[0] for x in funcs]
    funcs = [x[1] for x in funcs]
    excess_funcs = set(funcs_names) ^ {'get_float', 'error', 'squared_error', 'pipeline', 'calculate_zone'}
    assert excess_funcs == set(), excess_funcs
    for f in funcs:
        assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None
    assert module.DEFAULT_b0 == 1
    assert module.DEFAULT_b1 == 1
    assert module.SIGMA == 1


def test_func(**kwargs):
    stdin = kwargs[test.INPUT_stdin]
    args = kwargs[test.INPUT_args]
    stdout = kwargs[test.OUTPUT_stdout]
    rtrn = kwargs[test.OUTPUT_returned]
    
    assert stdin is None

    if rtrn is None:
        so_se, so_ez, res = stdout.split('\n')
        assert res == ''

        assert so_se[:4] == 'SE: '
        se = float(so_se[4:])
        
        a0 = float(args[0])
        a1 = float(args[1])
        e = 1+1*a0 - a1
        assert e**2 == se

        assert so_ez[:12] == 'Error zone: '
        assert L07_HW_project.calculate_zone(e) == so_ez[12:]
    elif isinstance(rtrn, ValueError):
        try:
            a0 = float(args[0])
            a1 = float(args[1])
            raise Exception
        except ValueError as e:
            assert isinstance(rtrn,ValueError)
    else:
        raise Exception


cases = [{test.INPUT_args: x, test.TEST_FUNC: test_func} for x in [
    [1, 5],
    [1, 6],
    [1, 3],
    [0, 0],
    [10, '2'],
    [10, '2asd'],
]]


def run(package_name):
    return test._run('L07_HW_project', cases, func_name='pipeline', test_module=test_module, package_name=package_name)
