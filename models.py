from flask_login import UserMixin, current_user
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    link = db.Column(db.String(2048))
    user_id = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(1000))