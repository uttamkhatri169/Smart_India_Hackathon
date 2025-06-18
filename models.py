from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class RawData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True)
    weekday = db.Column(db.String(10), index=True)
    delhi = db.Column(db.Float)
    brpl = db.Column(db.Float)
    bypl = db.Column(db.Float)
    ndmc = db.Column(db.Float)
    mes = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)  # Ensure this matches the CSV column name
    precipitation = db.Column(db.Float)

class OutputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True)
    weekday = db.Column(db.String(10), index=True)
    delhi = db.Column(db.Float)
    brpl = db.Column(db.Float)
    bypl = db.Column(db.Float)
    ndmc = db.Column(db.Float)
    mes = db.Column(db.Float)

class ComparisonData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, index=True)
    weekday = db.Column(db.String(10), index=True)
    delhi = db.Column(db.Float)
    brpl = db.Column(db.Float)
    bypl = db.Column(db.Float)
    ndmc = db.Column(db.Float)
    mes = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)