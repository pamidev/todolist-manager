# pip install -r requirements.txt
# python todolist_manager.py

import pickle
import sys
from dataclasses import dataclass

import click

DB_FILENAME = "todlist_database.db"


@dataclass
class TodoItem:
    id: int
    desc: str
    done: bool

    def __post_init__(self):
        if not self.desc:
            raise ValueError("Description cannot be empty.")
    

def find_new_id(todos: list[TodoItem]) -> int:
    ids = {todo.id for todo in todos}
    counter = 1
    while counter in ids:
        counter += 1
    return counter


def save_db(todos: list[TodoItem], overwrite: bool = True) -> None:
    mode = 'wb' if overwrite else 'xb'
    with open(DB_FILENAME, mode) as stream:
        pickle.dump(todos, stream)


def read_db_or_init() -> list[TodoItem]:
    try:
        with open(DB_FILENAME, 'rb') as stream:
            todos = pickle.load(stream)
    except FileNotFoundError:
        todos = []
    return todos


def print_todos(todos: list[TodoItem]) -> None:
    print(f"{'ID':>5} {'DONE?':^5} {'DECRIPTION'}")
    print("----- ----- ------------------------------")
    for todo in todos:
        if todo.done:
            done = '+'
        else:
            done = '-'
        print(f"{todo.id:5d} {done:^5} {todo.desc}")
    print("----- ----- ------------------------------")


def add_todo(description: str, todos: list[TodoItem]) -> None:
    todo = TodoItem(
        id=find_new_id(todos),
        desc=description,
        done=False
    )
    todos.append(todo)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--example', is_flag=True)
def init(example: bool) -> None:
    if example:
        todos = [
            TodoItem(id=1, desc='Example task 1', done=False),
            TodoItem(id=2, desc='Example task 2', done=True),
            TodoItem(id=3, desc='Example task 3', done=False),
        ]
    else:
        todos = []

    try:
        save_db(todos, overwrite=False)
    except FileExistsError:
        print(":-( Database is exist.")
    else:
        print(":-) Saved.")


@cli.command()
def list() -> None:
    todos = read_db_or_init()
    print_todos(todos)


@cli.command()
@click.argument('description')
def add(description: str) -> None:
    todos = read_db_or_init()

    try:
        add_todo(description, todos)
    except ValueError as e:
        print(f"ValueError: {e.args[0]}")
        sys.exit(0)

    save_db(todos)
    print(":-) Added new item to database.")


if __name__ == "__main__":
    cli()
