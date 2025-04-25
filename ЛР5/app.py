from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import CurrencyRates
import controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Rate(db.Model):
    id = db.Column(db.String(3), primary_key=True)
    datetime = db.Column(db.String(20), default="")
    value = db.Column(db.Float)

with app.app_context():
    db.create_all()

    currency_rates = CurrencyRates(db=db, Rate=Rate)

    if not Rate.query.first():
        currency_rates.fetch_rates()

    controller.init_controller(app, db, Rate, currency_rates)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)