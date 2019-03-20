from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from flask import render_template, flash, url_for, request

from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Flight


# TODO: tickets page


@app.route('/')
@app.route('/index')
@login_required
def index():
    flights = Flight.query.order_by(Flight.date_departure.desc())
    return render_template('index.html', title='Home', flights=flights)


@app.route('/flight/<id>')
@login_required
def flight(id):
    return render_template('flight.html', title='MOCKUP')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(
            user,
            remember=form.remember_me.data
        )
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template(
        'login.html',
        title='Sign In',
        form=form
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            address=form.address.data,
            postal_code=form.postal_code.data,
            country=form.country.data,
            state=form.state.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        title='Register',
        form=form
    )


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template(
        'user.html',
        user=user
    )


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(
            url_for(
                'user',
                username=current_user.username
            )
        )
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()