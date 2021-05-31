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
            return usr
        else: 
            return False

    @classmethod
    def user_from_form(cls, form):
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name= form.first_name.data
        last_name = form.last_name.data
        return cls.register(username, password, email, first_name, last_name)
