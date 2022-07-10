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


def get_module_test(task_name, package='hw_examples'):
    def body():
        return _test_module(task_name, package)
    return body
