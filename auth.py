
from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

from .models import User
from . import db


class SignUpForm(FlaskForm):
    first_name = StringField('first_name', validators=[
        DataRequired()])

    last_name = StringField('last_name', validators=[
        DataRequired()])

    email = StringField('email', validators=[
                        DataRequired(),
                        Email(message=Markup('&#9888; Ongeldig emailadres.'))])

    password = PasswordField('password', validators=[
        DataRequired(),
        Regexp(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
               message=Markup('&#9888; Wachtwoord moet minstens 8 karakters inclusief hoofdletter, kleine letter, cijfer en symbool bevatten.')),
        EqualTo('confirm', message=Markup('&#9888; Wachtwoorden niet identiek.'))])

    confirm = PasswordField('password', validators=[
        DataRequired()])


class LoginForm(FlaskForm):

    email = StringField('email', validators=[
                        DataRequired(),
                        Email(message=Markup('&#9888; Ongeldig emailadres.'))])

    password = PasswordField('password', validators=[
        DataRequired()])


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))

    form = LoginForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            email = request.form.get('email')
            password = request.form.get('password')

            # check if the user actually exists
            user = User.query.filter_by(email=email).first()

            # take the user-supplied password, hash it, and compare it to the hashed password in the database
            if not user or not check_password_hash(user.password, password):
                flash(Markup('&#9888; Email of wachtwoord onbekend.'))
                # if the user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login', form=form))

            # if the above check passes, then we know the user has the right credentials
            login_user(user)
            return redirect(url_for('main.projects'))
        
        else:
            flash(Markup('&#9888; Email of wachtwoord onbekend.'))
            return redirect(url_for('auth.login'))

    elif request.method == 'GET':
        return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))
    
    form = SignUpForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            # check if the user already exists
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                flash(Markup('&#9888; Emailadres al in gebruik.'))
                return render_template('signup.html', form=form)

            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(email=form.email.data, first_name=form.first_name.data.title(), last_name=form.last_name.data.title(),
                            password=generate_password_hash(form.password.data, method='sha256'))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash(Markup('&#128077; Account aangemaakt.'))
            return redirect(url_for('auth.login'))

        return render_template('signup.html', form=form)

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
