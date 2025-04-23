import requests
from bs4 import BeautifulSoup
import threading
import datetime


# Singleton Metaclass
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrencyRates(metaclass=Singleton):
    def __init__(self, app=None, db=None, currencies=None):
        if currencies is None:
            currencies = ['USD', 'EUR']  # Default currencies
        self.currencies = currencies
        self.rates = {}
        self.app = app
        self.db = db

        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        self.app = app
        self.db = db
        self.lock = threading.Lock()

        class Rate(db.Model):
            __tablename__ = 'currency_rates'  # Исправлено здесь!

            id = db.Column(db.String(3), primary_key=True)
            datetime = db.Column(db.String(20), default="")
            value = db.Column(db.Float)

            def __repr__(self):
                return f'<CurrencyRates {self.id}>'

        self.Rate = Rate  # Assign the Rate model to self

    def fetch_rates(self):
        try:
            url = 'http://www.cbr.ru/scripts/XML_daily.asp'
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.content, 'xml')
            new_rates = {}
            for valute in soup.find_all('Valute'):
                code = valute.CharCode.text
                if code in self.currencies:
                    rate = float(valute.Value.text.replace(',', '.'))
                    new_rates[code] = rate
            with self.lock:
                self.rates = new_rates
            self.save_to_db()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_rates(self):
        try:
            rates_from_db = self.Rate.query.all()  # Исправлено здесь!
            return {rate.id: rate.value for rate in rates_from_db}
        except Exception as e:
            print(f"Error loading rates from database: {e}")
            return {}

    def set_currencies(self, currencies):
        if not all(isinstance(c, str) and len(c) == 3 for c in currencies):
            raise ValueError("Currencies must be a list of 3-letter strings.")
        self.currencies = currencies
        self.fetch_rates()

    def save_to_db(self):
        try:
            for currency, rate in self.rates.items():
                existing_rate = self.Rate.query.filter_by(id=currency).first()  # Исправлено здесь!
                if existing_rate:
                    existing_rate.value = rate
                    existing_rate.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    new_rate = self.Rate(id=currency, value=rate, datetime=datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"))  # Исправлено здесь!
                    self.db.session.add(new_rate)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error saving to database: {e}")
            self.db.session.rollback()
            return False

    def load_from_db(self):
        try:
            rates_from_db = self.Rate.query.all()  # Исправлено здесь!
            self.rates = {rate.id: rate.value for rate in rates_from_db}
        except Exception as e:
            print(f"Error loading from database: {e}")

    def update_rate(self, currency_id, new_value):
        try:
            currency = self.Rate.query.filter_by(id=currency_id).first()  # Исправлено здесь!
            if currency:
                currency.value = new_value
                currency.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error updating rate in database: {e}")
            self.db.session.rollback()
            return False

    def create_rate(self, currency_id, new_value):
        try:
            currency = self.Rate.query.filter_by(id=currency_id).first()
            if currency:
                return False
            new_rate = self.Rate(id=currency_id, value=new_value,
                                 datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.db.session.add(new_rate)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error creating rate in database: {e}")
            self.db.session.rollback()
            return False

    def delete_rate(self, currency_id):
        try:
            currency = self.Rate.query.filter_by(id=currency_id).first()
            if currency:
                self.db.session.delete(currency)
                self.db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting rate in database: {e}")
            self.db.session.rollback()
            return False