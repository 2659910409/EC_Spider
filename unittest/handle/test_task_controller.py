from handle.task_controller import TaskController

if __name__ == '__main__':
    print('---------- start -------------')
    tc = TaskController('handle.task_creator.TaskCreator', {'store_ids': [1, 2, 3]})
    tc.run('task_init')
    tc.run('task_added')
    if not tc.is_success():
        print('-1-', tc.error)
        print('-1-', tc.error.print())
    tc.run('task_added123')
    if not tc.is_success():
        print('-2-', tc.error)
        print('-2-', tc.error.value.print())
    print('---------- end -------------')
