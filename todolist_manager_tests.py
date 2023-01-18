# pip install -r requirements.txt
# pytest todolist_manager_tests.py

from todolist_manager import find_new_id, read_db_or_init, save_db, TodoItem, add_todo


def test_empty_list():
    todos = []
    got = find_new_id(todos)
    assert got == 1


def test_single_todoitem_with_id_equals_one():
    todos = [TodoItem(id=1, desc='', done=False)]
    got = find_new_id(todos)
    assert got == 2


def test_single_todoitem_with_id_equals_two():
    todos = [TodoItem(id=2, desc='', done=False)]
    got = find_new_id(todos)
    assert got == 1


def test_multiple_todoitems():
    todos = [
        TodoItem(id=4, desc='', done=False),
        TodoItem(id=2, desc='', done=False),
        TodoItem(id=1, desc='', done=False),
    ]
    got = find_new_id(todos)
    assert got == 3


def test_add_todo():
    todos = [
        TodoItem(id=4, desc='', done=False),
        TodoItem(id=2, desc='', done=False),
        TodoItem(id=1, desc='', done=False),
    ]
    add_todo('description', todos)
    assert todos == [
        TodoItem(id=4, desc='', done=False),
        TodoItem(id=2, desc='', done=False),
        TodoItem(id=1, desc='', done=False),
        TodoItem(id=3, desc='description', done=False),
    ]


def test_persistance(tmpdir):
    with tmpdir.as_cwd():
        todos = [
            TodoItem(id=4, desc='', done=False),
            TodoItem(id=2, desc='', done=False),
            TodoItem(id=1, desc='', done=False),
        ]
    save_db(todos)
    got = read_db_or_init()
    assert got == todos
