from main_currency import CurrencyRates
from controllers import CurrencyRatesCRUD, ViewController, Controller

def main():
    try:
        currency_codes = ['USD', 'EUR', 'GBP']
        currency_rates = CurrencyRates(currency_codes)
        currency_rates_crud = CurrencyRatesCRUD()
        view_controller = ViewController()
        controller = Controller(currency_rates_crud, view_controller)

        rates_data = currency_rates.rates
        currency_rates_crud.create(rates_data)

        formatted_output = controller.get_currency_data()
        print(formatted_output)

        input("Проверка завершена. Нажмите Enter для выхода.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        currency_rates_crud.close()

if __name__ == "__main__":
    main()