
"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

#Making the application
APP = Flask(__name__)

#Making the route
@APP.route('/')

#Defining the function
def root():
    return "Air Quality"

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}>'.format(self.datetime)


    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        api = openaq.OpenAQ()
        res = api.measurements(city='Los Angeles', parameter='pm25', limit=10000, df=True)
        DB.session.add(res)
        DB.session.commit()
        return 'Data refreshed!'


    

