from hw_tests_prod import utils as test
from hw_examples import L10_HW_project
import inspect, types
import re, numpy as np


def test_module(module):
    classes = inspect.getmembers(module, inspect.isclass)
    assert len(classes)==3
    classes_names = [x[0] for x in classes]
    classes_ids = np.argsort(classes_names)

    assert classes_names[classes_ids[0]] == 'LinearRegression'
    assert classes_names[classes_ids[1]] == 'MLModel'
    assert classes_names[classes_ids[2]] == 'ZeroDataException'

    LinearRegression = classes[0][1]
    MLModel = classes[1][1]
    ZeroDataException = classes[2][1]

    assert hasattr(MLModel, 'fit')
    assert hasattr(MLModel, 'predict')
    ml = MLModel()
    ml.fit([1,2],[0,0])
    try:
        ml.fit([1,2],[0,0,2])
        raise Exception('MLModel.fit некорректно работает при len(X)!=len(Y)')
    except Exception as e:
        assert str(e) == 'Длина X должна быть равна длине Y'
    try:
        ml.fit([],[])
        raise Exception('MLModel.fit некорректно работает при len(X)==0')
    except ZeroDataException as e:
        pass

    init_code = inspect.getsource(LinearRegression.__init__)
    init_definition = init_code[:init_code.find(':')].replace('\n','').replace('\\','').replace(' ','')
    assert init_definition.startswith('def__init__(')
    assert init_definition.endswith(')')
    init_definition = init_definition[len('def__init__('):-1]
    init_kwargs = init_definition.split(',')
    
    assert 'b0=None' in init_kwargs, f"b0 в методе __init__ не равен None по умолчанию"
    assert 'b1=None' in init_kwargs, f"b1 в методе __init__ не равен None по умолчанию"

    code_fit = inspect.getsource(LinearRegression.fit)
    assert "super().fit(" in code_fit, f"В LinearRegression.fit не вызван родительский метод через super."
    
    code_predict = inspect.getsource(LinearRegression.predict)
    assert "super().predict(" in code_predict, f"В LinearRegression.predict не вызван родительский метод через super."

    methods = inspect.getmembers(LinearRegression, inspect.ismethod)
    lr = LinearRegression(3,-4)
    assert isinstance(lr, MLModel)
    assert lr.predict(2) == -5
    assert lr.predict(0) == 3
    lr.fit()
    assert lr.predict(2) == 3
    assert lr.predict(0) == 1
    assert isinstance(lr.evaluate, types.FunctionType), f"LinearRegression.evaluate не статический"
    assert lr.evaluate(3,5) == (-2,4)
    assert lr.evaluate(3,7) == (-4,16)

    lr = LinearRegression()
    assert -1<=lr.b0<=1
    assert -1<=lr.b1<=1
    assert -1<=module.init_weight()<=1

    all_vars = [x for x in inspect.getmembers(module) if not x[0].startswith('__')]
    all_vars_names = [x[0] for x in all_vars]
    excess_vars = set(all_vars_names) ^ {
        'normalvariate', 'get_float', 'init_weight', 'error', 'squared_error', 'pipeline', 'calculate_zone', \
            'MLModel', 'LinearRegression', 'ZeroDataException',}
    assert excess_vars == set()
    
    funcs = inspect.getmembers(module, inspect.isfunction)
    funcs_names = [x[0] for x in funcs]
    funcs = [x[1] for x in funcs]
    excess_funcs = set(funcs_names) ^ {'get_float', 'init_weight', 'error', 'squared_error', 'pipeline', 'calculate_zone'}
    assert excess_funcs == set(), excess_funcs
    for f in funcs:
        assert re.search('[a-zA-Zа-яА-Я]', f.__doc__) is not None


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
        assert L10_HW_project.calculate_zone(e, sigma=1, mu=0) == so_ez[12:]
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
    [10, 20],
]]


def run(package_name):
    return test._run('L10_HW_project', cases, func_name='pipeline', test_module=test_module, package_name=package_name)
