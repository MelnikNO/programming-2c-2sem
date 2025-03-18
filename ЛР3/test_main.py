import unittest
import sqlite3
import json
import sys
from io import StringIO
from main import trace

class MyTestCase(unittest.TestCase):
    def setUp(self):
        """Создает временное соединение с базой данных SQLite для тестов."""
        self.connection = sqlite3.connect(":memory:")
        # Создаем таблицу для хранения логов
        self.connection.execute("CREATE TABLE logtable (datetime TEXT, func_name TEXT, params TEXT, result TEXT)")

    def tearDown(self):
        """Закрывает соединение с базой данных после тестов."""
        self.connection.close()

    def test_trace_stdout(self):
        """Проверяет логирование вызова функции в стандартный вывод."""
        # Перенаправляем стандартный вывод в StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        @trace(handle=sys.stdout)
        def test_func(x):
            return x + 1

        test_func(1)

        # Возвращаем стандартный вывод обратно
        sys.stdout = sys.__stdout__

        # Проверяем, что вывод содержит данные в формате JSON
        output = captured_output.getvalue().strip()
        log_entry = json.loads(output)
        self.assertEqual(log_entry['func_name'], 'test_func')
        self.assertEqual(log_entry['params'], [1])
        self.assertEqual(log_entry['result'], 2)

    def test_trace_file_logging(self):
        """Проверяет логирование вызова функции в файл."""
        log_file = 'test_log.json'

        @trace(handle=log_file)
        def test_func(x):
            return x * 2

        test_func(3)

        with open(log_file, 'r') as f:
            output = f.readlines()

        # Проверяем, что файл не пуст и содержит корректные данные
        self.assertGreater(len(output), 0)
        log_entry = json.loads(output[0])
        self.assertEqual(log_entry['func_name'], 'test_func')
        self.assertEqual(log_entry['params'], [3])
        self.assertEqual(log_entry['result'], 6)

    def test_trace_sqlite_logging(self):
        """Проверяет логирование вызова функции в SQLite базу данных."""
        @trace(handle=self.connection)
        def test_func(x):
            return x - 1

        test_func(5)

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM logtable")
        rows = cursor.fetchall()

        # Проверяем, что запись была добавлена в базу данных
        self.assertEqual(len(rows), 1)
        log_entry = rows[0]

        self.assertIsNotNone(log_entry[0])  # datetime
        self.assertEqual(log_entry[1], 'test_func')
        self.assertEqual(json.loads(log_entry[2]), [5])  # params
        self.assertEqual(log_entry[3], '4')  # result


if __name__ == '__main__':
    unittest.main()
