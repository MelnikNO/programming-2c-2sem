# README.md

## Задание 
Реализовать параметризованный декоратор, который:
1) По умолчанию пишет в консоль (sys.stdout)
2) Может писать в текстовый файл в формате json (если передано имя файла '*.json') со следующей структурой одной записи:
- дата-время вызова функции, какая функция была вызвана и с какими параметрами и с каким результатом завершена.
- [{'datetime': '', 'func_name': 'str()', 'params': ['1','2', '3', ...], 'result': '...' }]
3) Может писать в базу данных sqlite3 (если передан объект типа sqlite3.Connection), развернутая в памяти компьютера
- не забыть предварительно создать таблицу для лога: cur = con.execute("INSERT INTO logtable VALUES (1234566, 'foo', '2', '4')")
- и записать в нее логи

"Рядом" с декоратором должна быть утилита, которая отображает содержимое базы данных с логированными данными

**Комментарий к основной программе:** 

**Результат основной программы:**


![code1](https://github.com/MelnikNO/programming-2c-2sem/blob/main/Screen/LR3/main.png)


**Комментарий к тестам:** 

**Результат тестовой программы:**

Unittest 

![test_code1](https://github.com/MelnikNO/programming-2c-2sem/blob/main/Screen/LR3/unittest.png)


Pytest

![test_code1](https://github.com/MelnikNO/programming-2c-2sem/blob/main/Screen/LR3/pytest.png)

