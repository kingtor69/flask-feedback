from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to psql database feedback_db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Model for users table, used for any given user in the system."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register new user w/hashed password & return that user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user model if valid, False if not"""

        usr = User.query.filter_by(username=username).first()
        if usr and bcrypt.check_password_hash(usr.password, pwd):
            session['username'] = username
            flash(f'You are now logged in, {usr.first_name}.', 'success')
            return usr
        else: 
            return False

    @classmethod
    def register_from_form(cls, form):
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name= form.first_name.data
        last_name = form.last_name.data
        session['username'] = username
        flash(f'Welcome. Successfully created your account, {first_name}. You are now logged in as {username}.', 'success')
        return cls.register(username, password, email, first_name, last_name)

class Feedback(db.Model):
    """Model for feedback table, used for valid users giving feedback with username is foreign key."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'))

    user = db.relationship('User', backref="feedback")