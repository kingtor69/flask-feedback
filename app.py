from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUserForm
from sqlalchemy.exc import IntegrityError

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
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_new_user():
    """load form for new user and process that input, creating a new user in the database"""

    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name= form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
    
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Try again, ya' twit.")
            return render_template('register.html', form=form)
        
        session['username'] = new_user.username
        flash('Welcome. Successfully created your account. You are now logged in.', 'success')

        return redirect('/')

        
    
    # don't forget in validating to add unique test for username

    return render_template('register.html', form=form)