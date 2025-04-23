from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


with app.app_context():
    if not os.path.exists('database.db'):
        db.create_all()

        from model import CurrencyRates as CurrencyRatesModel
        currency_rates_instance = CurrencyRatesModel(app=app, db=db)
        usd = currency_rates_instance.Rate.query.filter_by(id='USD').first()
        gbp = currency_rates_instance.Rate.query.filter_by(id='GBP').first()
        eur = currency_rates_instance.Rate.query.filter_by(id='EUR').first()

        if not usd:
            usd = currency_rates_instance.Rate(id='USD', value=90.9)
            db.session.add(usd)
        if not gbp:
            gbp = currency_rates_instance.Rate(id='GBP', value=100.9)
            db.session.add(gbp)
        if not eur:
            eur = currency_rates_instance.Rate(id='EUR', value=91.0)
            db.session.add(eur)

        db.session.commit()

controller.init_controller(app,db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)