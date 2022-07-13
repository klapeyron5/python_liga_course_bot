from multiprocessing import Pool
import importlib

package = 'hw_examples'

tasks = [
    'L04_HW_task1',
    'L04_HW_task2',
    'L04_HW_task3',
    'L04_HW_project',
    'L05_HW_task1'
    'L05_HW_project',
]

def f(task):
    m = importlib.import_module('hw_tests.test_'+task)
    res, log = m.run(package)
    return res, log

res = {}
pool = Pool(len(tasks))

args = [list((x,)) for x in tasks]
outs = pool.starmap(f, args)

passed = 0
for task, out in zip(tasks, outs):
    passed += out[0]
print(f'Успешно протестировано {passed} ДЗ из {len(tasks)}')
for task, out in zip(tasks, outs):
    if not out[0]:
        print(f'Провалено задание {task}: {out[1]}')