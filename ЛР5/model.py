import requests
from bs4 import BeautifulSoup
import datetime

class CurrencyRates:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, db=None, Rate=None, currencies=None):
        if not hasattr(self, 'initialized'):
            if currencies is None:
                currencies = ['USD', 'EUR', 'GBP']
            self.currencies = currencies
            self.rates = {}
            self.db = db
            self.Rate = Rate
            self.initialized = True
            self.fetch_rates()

    def fetch_rates(self):
        try:
            url = 'http://www.cbr.ru/scripts/XML_daily.asp'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            new_rates = {}
            for valute in soup.find_all('Valute'):
                code = valute.CharCode.text
                if code in self.currencies:
                    rate = float(valute.Value.text.replace(',', '.'))
                    new_rates[code] = rate
            self.rates = new_rates
            self.save_to_db()
            return True
        except Exception as e:
            print(f"Error fetching rates: {e}")
            return False

    def get_rates(self):
        try:
            rates_from_db = self.Rate.query.all()
            rates = {rate.id: {'value': rate.value, 'datetime': rate.datetime} for rate in rates_from_db if rate.id in self.currencies}
            return rates
        except Exception as e:
            print(f"Error getting rates: {e}")
            return {}

    def set_currencies(self, currencies):
         if not all(isinstance(c, str) and len(c) == 3 for c in currencies):
            raise ValueError("Currencies must be a list of 3-letter strings.")
         self.currencies = currencies
         self.fetch_rates()


    def save_to_db(self):
        try:
            for currency, rate in self.rates.items():
                existing_rate = self.Rate.query.filter_by(id=currency).first()
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if existing_rate:
                    existing_rate.value = rate
                    existing_rate.datetime = now
                else:
                    new_rate = self.Rate(id=currency, value=rate, datetime=now)
                    self.db.session.add(new_rate)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error saving to db: {e}")
            return False

    def update_rate(self, currency_id):
        try:
            self.fetch_rates()
            if currency_id in self.rates:
                currency = self.Rate.query.filter_by(id=currency_id).first()
                currency.value = self.rates[currency_id]
                currency.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(f"Error during update: {e}")
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
            print(f"Error during delete: {e}")
            return False