from app import db, login
from datetime import datetime
from flask_login import UserMixin


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False, unique=True)
    last_name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    home_address = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def delete_con(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'First Name', 'Last name', "Phone Number", 'Home Address'}:
                setattr(self, key, value)
        db.session.commit()

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

@login.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    user_name = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Address_Book = db.relationship('Book', backref='author', lazy='dynamic')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.username

    def pass_check(self, guess):
        if self.password == guess:
            return 'congrats'
