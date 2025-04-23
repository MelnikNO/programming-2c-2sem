from flask import render_template, request, redirect, url_for

from model import CurrencyRates


def init_controller(app, db):
    currency_rates = CurrencyRates(app=app, db=db)

    @app.route('/')
    def index():
        try:
            rates = currency_rates.get_rates()
            return render_template('index.html', rates=rates)
        except Exception as e:
            return f"An error occurred: {e}"

    @app.route('/update', methods=['GET', 'POST'])
    def update():
        if request.method == 'POST':
            try:
                currency_id = request.form['currency_id'].upper()
                new_value = float(request.form['new_value'])

                success = currency_rates.update_rate(currency_id, new_value)

                if success:
                    return redirect(url_for('index'))
                else:
                    return render_template('update.html', error_message="Currency not found")

            except ValueError:
                return render_template('update.html', error_message="Invalid input")
            except Exception as e:
                return render_template('update.html', error_message=f"An error occurred: {e}")
        else:
            return render_template('update.html')

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            try:
                currency_id = request.form['currency_id'].upper()
                new_value = float(request.form['new_value'])

                success = currency_rates.create_rate(currency_id, new_value)

                if success:
                    return redirect(url_for('index'))
                else:
                    return render_template('create.html', error_message="Currency already exists")

            except ValueError:
                return render_template('create.html', error_message="Invalid input")
            except Exception as e:
                return render_template('create.html', error_message=f"An error occurred: {e}")
        else:
            return render_template('create.html')

    @app.route('/delete/<currency_id>')
    def delete(currency_id):
        try:
            success = currency_rates.delete_rate(currency_id)
            if success:
                return redirect(url_for('index'))
            else:
                return render_template('index.html', error_message="Currency not found")
        except Exception as e:
            return render_template('index.html', error_message=f"An error occurred: {e}")