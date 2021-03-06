from hw_tests.utils import run

package = 'hw_examples'

tasks = [
    'L04_HW_task1',
    'L04_HW_task2',
    'L04_HW_task3',
    'L04_HW_project',
    'L05_HW_task1',
    'L05_HW_project',
    'L06_HW_task1',
    'L06_HW_task2',
]

outs = [run(t, package) for t in tasks]

passed = 0
for task, out in zip(tasks, outs):
    passed += out[0]
print(f'Успешно протестировано {passed} ДЗ из {len(tasks)}')
for task, out in zip(tasks, outs):
    if not out[0]:
        print(f'Провалено задание {task}: {out[1]}')
