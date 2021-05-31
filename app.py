from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUserForm, LoginForm
from sqlalchemy.exc import IntegrityError
from helpers import secrets
from random import choice

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "this_B_secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def load_home_page():
    """load home page"""
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_new_user():
    """load form for new user and process that input, creating a new user in the database"""

    form = RegisterUserForm()
    if form.validate_on_submit():
        # username = form.username.data
        # password = form.password.data
        # email = form.email.data
        # first_name= form.first_name.data
        # last_name = form.last_name.data
        # new_user = User.register(username, password, email, first_name, last_name)
        new_user = User.register_from_form(form)
    
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Try again, ya' twit.")
            return render_template('register.html', form=form)
        
        session['username'] = new_user.username
        flash('Welcome. Successfully created your account. You are now logged in.', 'success')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """log and existing user into the site, 
    create a session for that user, 
    post error if authentication fails,
    offer link to registration."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            flash(f'You are now logged in, {user.first_name}.', 'success')
            return redirect(f'/users/{user.username}')
        flash('invalid username/password combination', 'danger')

    return render_template('login.html', form=form)

@app.route('/secret')
def display_secret_message():
    """display a secret message for valid, logged-in users;
    redirect unauthorized visitors to login screen with flashed message"""
    if 'username' in session:
        secret = choice(secrets)
        return render_template('secret.html', secret=secret)
    flash('only logged in users can view secrets', 'danger')
    return redirect('/login')

@app.route('/users/<username>')
def display_user_public_profile(username):
    """display all public information we have on a given user
    in this case 'public' meaning validated, logged-in users"""
    if 'username' in session:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)
    flash('only logged in users can view that page', 'warning')
    return redirect('/')

@app.route('/logout', methods=['POST'])
def logout():
    """log out of site and redirect to home"""
    session.pop("username")
    flash('You have successfully logged out.', 'info')
    return redirect('/')