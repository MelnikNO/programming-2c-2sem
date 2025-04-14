import requests
from xml.etree import ElementTree
from singleton import Singleton

class CurrencyRates(metaclass=Singleton):
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"

    def __init__(self, char_codes=None):
        self._rates = {}
        self._char_codes = None

        if char_codes is None:
            char_codes = ['USD', 'EUR', 'GBP']

        if self._check_char_codes(char_codes):
            self._char_codes = char_codes
            self._fetch_rates()
        else:
            raise ValueError('Some char code is not correct')

    @property
    def rates(self):
        return self._rates

    @property
    def char_codes(self):
        return self._char_codes

    @char_codes.setter
    def char_codes(self, new_char_codes):
        if not isinstance(new_char_codes, list):
            raise TypeError("char_codes must be a list")
        if not all(isinstance(code, str) and len(code) == 3 for code in new_char_codes):
            raise ValueError("Each char code must be a string of length 3")

        if self._check_char_codes(new_char_codes):
            self._char_codes = new_char_codes
            self._fetch_rates()
        else:
            raise ValueError('Some char code is not correct')

    @char_codes.deleter
    def char_codes(self):
        self._char_codes = None

    def _check_char_codes(self, char_codes):
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
            tree = ElementTree.fromstring(response.content)
            available_codes = [code.text for code in tree.findall('.//CharCode')]
            return all(code in available_codes for code in char_codes)
        except requests.exceptions.RequestException as e:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")
        except Exception as e:
            raise Exception(f"Error parsing {e}")

    def _fetch_rates(self):
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
            tree = ElementTree.fromstring(response.content)
            self._rates = {}
            for valute in tree.findall('.//Valute'):
                char_code = valute.find('CharCode').text
                if char_code in self._char_codes:
                    value_element = valute.find('Value')
                    if value_element is not None:
                        value = float(value_element.text.replace(",", "."))
                        self._rates[char_code] = value
        except requests.exceptions.RequestException as e:
            raise ConnectionError("Не удалось получить данные с сайта ЦБ РФ")
        except Exception as e:
            raise Exception(f"Error parsing {e}")

# Пример использования
if __name__ == "__main__":
    c_r = CurrencyRates()

    print(c_r.rates)
    # print("Курс USD:", c_r.rates.get("USD"))