from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Artist(UserMixin, db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    artistid = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
