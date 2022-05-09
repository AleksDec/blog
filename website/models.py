from . import db 
from flask_login import UserMixin
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()

class User(db.Model, UserMixin):
    __tablename__ = os.getenv('TABLENAME_U')
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    posts = db.relationship('BlogPost', backref='author')

class BlogPost(db.Model):
    __tablename__ = os.getenv('TABLENAME_B')
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # Foreign Key to link Users (refer to primary key of a user)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))