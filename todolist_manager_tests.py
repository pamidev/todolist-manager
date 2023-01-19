# pip install -r requirements.txt
# pytest todolist_manager_tests.py

from todolist_manager import find_new_id, read_db_or_init, save_db, TodoItem, add_todo


def test_empty_list():
    todos = []
    got = find_new_id(todos)
    assert got == 1


def test_single_todoitem_with_id_equals_one():
    todos = [TodoItem(id=1, desc='description', done=False)]
    got = find_new_id(todos)
    assert got == 2


def test_single_todoitem_with_id_equals_two():
    todos = [TodoItem(id=2, desc='description', done=False)]
    got = find_new_id(todos)
    assert got == 1


def test_multiple_todoitems():
    todos = [
        TodoItem(id=4, desc='description4', done=False),
        TodoItem(id=2, desc='description2', done=False),
        TodoItem(id=1, desc='description1', done=False),
    ]
    got = find_new_id(todos)
    assert got == 3


def test_add_todo():
    todos = [
        TodoItem(id=4, desc='description4', done=False),
        TodoItem(id=2, desc='description2', done=False),
        TodoItem(id=1, desc='description1', done=False),
    ]
    add_todo('description3', todos)
    assert todos == [
        TodoItem(id=4, desc='description4', done=False),
        TodoItem(id=2, desc='description2', done=False),
        TodoItem(id=1, desc='description1', done=False),
        TodoItem(id=3, desc='description3', done=False),
    ]


def test_persistance(tmpdir):
    with tmpdir.as_cwd():
        todos = [
            TodoItem(id=4, desc='description4', done=False),
            TodoItem(id=2, desc='description2', done=False),
            TodoItem(id=1, desc='description1', done=False)
        ]
    save_db(todos)
    got = read_db_or_init()
    assert got == todos
