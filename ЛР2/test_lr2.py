import unittest
from lr2main import main
from lr2main import setup_data
from lr2main import calculate_time

class Testbinarytree(unittest.TestCase):
    def test_main_functionality(self):
        """Тестирует, что функция main выполняется без ошибок."""
        try:
            main()
        except Exception as e:
            self.fail(f"main() вызвал исключение: {e}") # Если возникает ошибка, тест не проходит

    def test_setup_data(self):
        """Тестирует функцию setup_data на корректность возвращаемых данных."""
        result = setup_data(3)
        self.assertEqual(len(result), 3)
        # Проверяем, что результат соответствует ожидаемым значениям
        expected = [(0, 0), (1, 2), (2, 4)]
        self.assertEqual(result, expected)

    def test_calculate_time_positive(self):
        """Тестирует функцию calculate_time на положительном примере."""
        data = [(i, i + 1) for i in range(100)]

        # Определяем вспомогательную функцию для тестирования времени выполнения
        def dummy_func(root, height):
            result = 0
            for _ in range(10000):  # Увеличиваем количество итераций для нагрузки
                result += root + height
            return result

        time_taken = calculate_time(data, dummy_func)
        self.assertIsInstance(time_taken, float) # Проверяем, что возвращаемое значение - это число с плавающей запятой
        self.assertGreater(time_taken, 0) # Проверяем, что время выполнения больше нуля


if __name__ == '__main__':
    unittest.main()
