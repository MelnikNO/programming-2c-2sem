import sys
import functools
import sqlite3
import json
from datetime import datetime

# параметризованный декоратор
# def trace(func):
def trace(func=None, *, handle=sys.stdout):
    """
    Логирование происходит в:
    - стандартный вывод (sys.stdout или sys.stderr)
    - файл в формате JSON
    - базу данных SQLite

    :param func: Функция, которую необходимо обернуть декоратором. Если не указана, возвращает функцию-декоратор.
    :param handle: Место для логирования. Может быть стандартным выводом, именем файла для записи в формате JSON или соединением с SQLite.
    :return: Обернутую функцию с логированием.
    """

    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        # Создаем запись лога
        log_entry = {
            'datetime': datetime.now().isoformat(),
            'func_name': func.__name__,
            'params': args,
            'result': None
        }

        # Вызов оригинальной функции и получение результата
        result = func(*args, **kwargs)
        log_entry['result'] = result

        # Логирование в консоль или stderr
        if handle == sys.stdout or handle == sys.stderr:
            handle.write(json.dumps(log_entry) + "\n")

        # Логирование в файл JSON
        elif isinstance(handle, str) and handle.endswith('.json'):
            with open(handle, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

        # Логирование в SQLite базу данных
        elif isinstance(handle, sqlite3.Connection):
            cur = handle.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS logtable (datetime TEXT, func_name TEXT, params TEXT, result TEXT)")
            cur.execute("INSERT INTO logtable (datetime, func_name, params, result) VALUES (?, ?, ?, ?)",(log_entry['datetime'], log_entry['func_name'], json.dumps(log_entry['params']), str(result)))
            handle.commit()

        return result

    return inner


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
@trace(handle=sys.stderr)
def increm(x):
    """Инкремент"""
    return x + 1

@trace(handle=sys.stdout)
def decrem(x):
    """Декремент"""
    return x - 1

print(increm.__doc__)
print(increm(2))
print(decrem(2))

@trace()  # Вариант по умолчанию (логирование в stderr)
def f2(x):
    return x ** 2

@trace(handle='logger.json')  # Логирование в файл JSON
def f3(x):
    return x ** 3

# Создаем базу данных в памяти для логирования
handle_for_f4 = sqlite3.connect(":memory:")
@trace(handle=handle_for_f4)  # Логирование в SQLite
def f4(x):
    return x ** 4

# Вызов функций для тестирования
increm(2)
decrem(2)
f2(3)
f3(4)
f4(5)

# Отображение логов из базы данных
showlogs(handle_for_f4)

# Закрытие соединения с базой данных
handle_for_f4.close()
