import sys
import importlib


def _test_module(task_name, package):
    global module
    task_name = package+'.'+task_name
    if 'hw_examples' not in sys.modules:
        module = importlib.import_module(task_name)
    else:
        importlib.reload(module)
    return module


def get_module_test(module_name, package='hw_examples'):
    if not check_task_name_format(module_name):
        raise Exception(f'Wrong format of tested module name: {module_name}')
    def body():
        return _test_module(module_name, package)
    return body


def check_task_name_format(tn):
    """
    Examples of right formats:
    L04_HW_project
    L11_HW_task1
    L09_HW_task10
    """
    try:
        assert tn[0] == 'L'
        L = int(tn[1:3])
        assert L >= 1
        assert tn[3:7] == '_HW_'
        c0 = tn[7:] == 'project'
        try:
            task_number = int(tn[11:])
        except:
            task_number = 0
        c1 = tn[7:11] == 'task' and task_number >= 1 and len(str(task_number)) == len(tn[11:])
        assert c0 or c1
        return 1
    except:
        return 0
