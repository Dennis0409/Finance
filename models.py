from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class TransactionType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    type = db.Column(db.Enum(TransactionType),nullable = False)
    category = db.Column(db.String,nullable = False)
    amount = db.Column(db.Float,nullable = False)
    date = db.Column(db.DateTime,nullable = False)
    note = db.Column(db.Text,nullable = True)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)

def init_db(app):
    db.init_app(app)
    return db