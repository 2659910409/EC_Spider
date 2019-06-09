from handle.task_controller import TaskController

if __name__ == '__main__':
    print('----------123-------------')
    tc = TaskController('handle.task_creator.TaskCreator', {'store_ids': [1, 2, 3]})
    tc.run('task_init')
    tc.run('task_added')
    if tc.is_error():
        print('-1-', tc.error)
        print('-1-', tc.error.value)
    tc.run('task_added123')
    if tc.is_error():
        print('-2-', tc.error)
        print('-2-', tc.error.value.get_err_msg())
    print('----------456-------------')
