from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[Length(max=20, message="That username is too long. Please try a username 20 characters or shorter"), InputRequired(message="Please enter a username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])
    email = StringField("email address", validators=[Email(message="Please enter a valid email address")])
    first_name = StringField("First Name", validators=[Length(max=30, message="Sorry, your first name as entered is too long for our database. Please enter a shortened version."), InputRequired(message="Please enter your first name.")])
    last_name = StringField("Last Name", validators=[Length(max=30, message="Sorry, your last name as entered is too long for our database. Please enter a shortened version."), InputRequired(message="Please enter your last name.")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Please enter a username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a password")])

class DeleteUserForm(FlaskForm):
    confirmation = StringField("To confirm you want to delete, please type your username:")