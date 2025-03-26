import sys
import functools
import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager


# параметризованный декоратор
# def trace(func):
def trace(func=None, *, handle=sys.stdout):

    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        log_entry = {
            'datetime': datetime.now().isoformat(),
            'func_name': func.__name__,
            'params': args,
            'result': None
        }

        result = func(*args, **kwargs)
        log_entry['result'] = result

        if handle == sys.stdout:
            handle.write(json.dumps(log_entry) + "\n")

        elif isinstance(handle, str) and handle.endswith('.json'):
            with open(handle, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

        return result

    return inner


@contextmanager
def dbc():
    handle_for_f4 = sqlite3.connect(":memory:")
    try:
        print('connection to db')
        yield handle_for_f4
    finally:
        print('handle is closing')
        handle_for_f4.close()


def showlogs(con: sqlite3.Connection):
    """
    Отображает логи из базы данных SQLite.
    :param con: Соединение с базой данных SQLite, из которой будут извлечены логи.
    :return: None
    """

    cur = con.cursor()
    cur.execute("SELECT * FROM logtable")
    rows = cur.fetchall()
    for row in rows:
        print(row)


# Пример использования декоратора
@trace(handle=sys.stdout)
def increm(x):
    """Инкремент"""
    return x + 1


@trace(handle=sys.stdout)
def decrem(x):
    """Декремент"""
    return x - 1


@trace()
def f2(x):
    return x ** 2


@trace(handle='loggercontextmanager.json')  # Логирование в файл JSON
def f3(x):
    return x ** 3


def main():
    print(increm.__doc__)
    print(increm(2))
    print(decrem(2))

    # менеджера контекста
    with dbc() as handle_for_f4:
        @trace(handle=handle_for_f4.cursor())
        def f4(x):
            """Четвертая степень"""
            return x ** 4

        print(f4(10))

        # Вызов функций для тестирования
        increm(2)
        decrem(2)
        f2(3)
        f3(4)


if __name__ == "__main__":
    main()

