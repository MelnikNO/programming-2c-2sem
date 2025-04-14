# контроллер для работы с БД при использовании класса currencyrates

import sqlite3
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Model (Работа с БД)
class CurrencyRatesCRUD:
    def __init__(self, db_name='currency.db'):
        self.__con = sqlite3.connect(db_name)
        self.__con.row_factory = sqlite3.Row
        self.__cursor = self.__con.cursor()
        self.__createtable()

    def __createtable(self):
        try:
            self.__cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cur TEXT NOT NULL,
                    datetime TEXT NOT NULL,
                    value REAL NOT NULL
                )
                """
            )
            self.__con.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def create(self, currency_rates):
        try:
            sql_query = "INSERT INTO currency (cur, datetime, value) VALUES (:cur, :datetime, :value)"
            params = [{'cur': cur, 'datetime': datetime.now().isoformat(), 'value': value}
                      for cur, value in currency_rates.items()]
            self.__cursor.executemany(sql_query, params)
            self.__con.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении данных: {e}")

    def read(self, cur=None):
        try:
            sql_query = "SELECT * FROM currency WHERE 1=1"
            params = {}
            if cur:
                sql_query += " AND cur = :cur"
                params['cur'] = cur
            self.__cursor.execute(sql_query, params)
            rows = self.__cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Ошибка при чтении данных: {e}")
            return []

    def update(self, cur, new_value):
        try:
            sql_query = "UPDATE currency SET value = :new_value WHERE cur = :cur"
            params = {'new_value': new_value, 'cur': cur}
            self.__cursor.execute(sql_query, params)
            self.__con.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении данных: {e}")

    def delete(self, cur):
        try:
            sql_query = "DELETE FROM currency WHERE cur = :cur"
            params = {'cur': cur}
            self.__cursor.execute(sql_query, params)
            self.__con.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении данных: {e}")

    def close(self):
        if self.__con:
            self.__con.close()
            self.__con = None
            self.__cursor = None

# View (Отображение)
class ViewController:
    def __init__(self, template_dir='templates'):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def render_template(self, template_name, data):
        template = self.env.get_template(template_name)
        return template.render(data=data)

# Controller
class Controller:
    def __init__(self, currency_rates_crud, view_controller):
        self.db_crud = currency_rates_crud
        self.view_controller = view_controller

    def get_currency_data(self):
        try:
            from main_currency import CurrencyRates
            currency_codes = ['USD', 'EUR', 'GBP']
            currency_rates = CurrencyRates(currency_codes)
            rates = currency_rates.rates
            self.db_crud.create(rates)
            all_data = self.db_crud.read()
            now = datetime.now().isoformat()
            data = {'datetime': now, 'currencies': all_data}
            return self.view_controller.render_template('currency_jinja2.html', data)
        except Exception as e:
            return f"Произошла общая ошибка: {e}"