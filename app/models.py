import jwt
from time import time
from app import db, login
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    pass_hash = db.Column(db.String(128))
    notes = db.relationship('Card', backref='payer', lazy='dynamic')

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def create_token(self, exp=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + exp},
                          key=current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id_ = jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms='HS256')['reset_password']
        except jwt.InvalidTokenError:
            return
        return User.query.get(id_)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, index=True)
    category = db.Column(db.String(16), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    note = db.Column(db.String(32), index=True)
    kind = db.Column(db.Boolean, index=True)
    year = db.Column(db.Integer, default=datetime.utcnow().date().year)
    month = db.Column(db.Integer, default=datetime.utcnow().date().month)
    day = db.Column(db.Integer, default=datetime.utcnow().date().day)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<{}, {}, {}, {}, {}>'.format(self.id, self.price,
                                             self.category, self.note,
                                             self.user_id)


@login.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))
