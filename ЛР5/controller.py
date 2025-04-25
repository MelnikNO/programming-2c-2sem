from flask import render_template, request, redirect, url_for

def init_controller(app, db, Rate, currency_rates):

    @app.route('/', methods=['GET', 'POST'])
    def index():
         if request.method == 'POST':
            currencies = request.form['currencies'].upper().split(',')
            currencies = [c.strip() for c in currencies]
            currency_rates.set_currencies(currencies)
            return redirect(url_for('index'))
         rates = currency_rates.get_rates()
         return render_template('index.html', rates=rates, currency_rates = currency_rates)


    @app.route('/update/<currency_id>', methods=['GET', 'POST'])
    def update(currency_id):
        if request.method == 'POST':
            currency_rates.update_rate(currency_id)
            return redirect(url_for('index'))
        else:
            return render_template('update.html', currency_id=currency_id)

    @app.route('/delete/<currency_id>', methods=['POST'])
    def delete(currency_id):
        currency = Rate.query.filter_by(id=currency_id).first()
        if currency:
            currency_rates.delete_rate(currency_id)
        return redirect(url_for('index'))

    @app.route('/set_currencies', methods=['POST'])
    def set_currencies():
        currencies = request.form['currencies'].upper().split(',')
        currencies = [c.strip() for c in currencies]
        try:
            currency_rates.set_currencies(currencies)
        except ValueError as e:
            print(f"Error setting currencies: {e}")
        return redirect(url_for('index'))