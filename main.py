from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from .models import Project
from . import db

main = Blueprint('main', __name__)


class ProjectForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    link = StringField('link', validators=[DataRequired()])


@main.route('/')
def index():

    if current_user.is_authenticated:
        return redirect(url_for('main.projects'))
    else:
        return redirect(url_for('auth.login'))


@main.route('/all_projects')
@login_required
def all_projects():

    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('all_projects.html', projects=projects)


@main.route('/projects')
@login_required
def projects():

    user_projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.id.desc())
    return render_template('projects.html', user_projects=user_projects)


@main.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():

    form = ProjectForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            title = request.form.get('title')
            descripton = request.form.get('description')
            link = request.form.get('link')
            author = current_user.first_name + ' ' + current_user.last_name

            # create a new project with the form data.
            new_project = Project(title=title, description=descripton, link=link, user_id=current_user.id, author=author)

            # add the new user to the database
            db.session.add(new_project)
            db.session.commit()
            flash(Markup('&#128077; Project aangemaakt.'))
            return redirect(url_for('main.projects'))

    elif request.method == 'GET':
        return render_template('new_project.html', form=form)
