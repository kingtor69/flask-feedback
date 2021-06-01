from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginForm, DeleteUserForm, FeedbackForm
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
    return redirect('/users')

################## register/login/logout routes
@app.route('/register', methods=['GET', 'POST'])
def register_new_user():
    """load form for new user and process that input, creating a new user in the database"""

    form = RegisterUserForm()
    if form.validate_on_submit():
        new_user = User.register_from_form(form)
    
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Try again, ya' twit.")
            return render_template('register.html', form=form)
        
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
            return redirect(f'/users/{user.username}')
        flash('invalid username/password combination', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout():
    """log out of site and redirect to home"""
    session.pop("username")
    flash('You have successfully logged out.', 'info')
    return redirect('/')

########### secret route
@app.route('/secret')
def display_secret_message():
    """display a secret message for valid, logged-in users;
    redirect unauthorized visitors to login screen with flashed message"""
    if 'username' in session:
        secret = choice(secrets)
        return render_template('secret.html', secret=secret)
    flash('only logged in users can view secrets', 'danger')
    return redirect('/login')

##################### users routes
@app.route('/users')
def display_user_list():
    """displays a list of all users with usernames only for anyone who is not logged in, and full profile information for valid, logged-in users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<username>')
def display_user_public_profile(username):
    """display all public information we have on a given user
    in this case 'public' meaning validated, logged-in users"""
    if 'username' in session:
        user = User.query.get_or_404(username)
        # TODO: either this feedback isn't loading properly, or user.html isn't displaying it properly
        user_feedback = Feedback.query.filter_by(username=username).all() or None
        # ...and 'or None' is not the problem
        return render_template('user.html', user=user, feedback=user_feedback)

    flash('only logged in users can view that page', 'warning')
    return redirect('/')

@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def confirm_delete_user_and_feedback(username):
    """Delete a user and all of their feedback. 
    A user can only be deleted by themselves, 
    so return an error if the user to be deleted is not logged in."""
    user = User.query.get_or_404(username)
    # if this page is to delete any other than logged in user, 
    # redirect to home page
    if not username == session["username"]:
        flash('only a logged in user can delete themself', 'danger')
        return redirect('/')

    session.pop("username")
    db.session.delete(user)
    feedback_of_user = Feedback.query.filter_by(username=username)
    for feedback in feedback_of_user:
        db.session.delete(feedback)
    db.session.commit()
    flash(f'user {username} has been deleted, along with all their feedback', 'warning')
    return redirect('/')


    # TODO for future delevelopment:
    # I didn't get this rabbithole to work
    form = DeleteUserForm()

    # if they really wanted to do this, do it;
    # redirect to their user page if they did not
    if form.validate_on_submit():
        confirmation = form.confirmation.data
        if confirmation == username:
            session.pop("username")
            feedback_of_user = Feedback.query.filter_by(username=username)
            db.session.delete(user)
            for feedback in feedback_of_user:
                db.session.delete(feedback)
            db.session.commit()
            return redirect('/')
        else:
            flash('user deletion neither confirmed nor executed', 'info')
            return redirect(f'/users/{username}')

    # confirm they really want to delete themselves
    return render_template('delete.html', user=user, form=form)
                
##################### feedback routes
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def new_feedback_form(username):
    if not session['username'] == username:
        if session['username']:
            logged_in_username = session['username']
            return redirect(f'/users/{loggin_in_username}/feedback/add')
        else:
            flash('Only logged-in users can post feedback', 'info')
            return redirect('/login')

    form = FeedbackForm()
    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    # TODO: error messages in this template are wrong, shows "content" on both fields if there's an error on either 
    return render_template('feedback.html', user=user, form=form)
        