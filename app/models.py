from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_magazine = db.Table('user_magazine',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('magazine_id', db.Integer, db.ForeignKey('magazine.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    subscriptions = db.relationship('Magazine', secondary=user_magazine, backref='subscribers')

    def __init__(self, name, address):
        self.name = name
        self.address = address

class Magazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name