from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from flask import render_template, flash, url_for, request, g

from app.forms import LoginForm, RegistrationForm, EditProfileForm, SearchForm
from app.models import User, Flight, Ticket
from app.errors.handlers import not_found_error


@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    flights = db.session.query(User, Flight).join("flights").filter(current_user.id == Ticket.user_id).paginate(page, 6, False)
    flights_dto = [flight[1] for flight in flights.items]
    next_url = url_for('index', page=flights.next_num) if flights.has_next else None
    prev_url = url_for('index', page=flights.prev_num) if flights.has_prev else None
    return render_template('index.html', title='Home', flights=flights_dto, next_url=next_url, prev_url=prev_url)


@app.route('/admin')
@login_required
def admin():
    if current_user.role_id != 2:
        return redirect(url_for('index'))
    return "ADMEN"


@app.route('/ticket/<id>/buy')
def buy_ticket(id):
    current_user.buy_ticket(id)
    db.session.commit()
    return render_template('ticket_status.html', title='Ticket was bought')


@app.route('/ticket/<id>/revoke')
def revoke_ticket(id):
    current_user.revoke_ticket(id)
    db.session.commit()
    return render_template('ticket_status.html', title='Ticket was revoked')


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    flights = Flight.query.order_by(Flight.date_departure.desc()).paginate(page, 6, False)
    next_url = url_for('explore', page=flights.next_num) if flights.has_next else None
    prev_url = url_for('explore', page=flights.prev_num) if flights.has_prev else None
    return render_template(
        'explore.html',
        title='Explore',
        flights=flights.items,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/flights/<flight_id>')
@login_required
def flight(flight_id):
    flight = Flight.query.filter_by(id=flight_id).first()
    if not flight.active:
        return not_found_error(404)
    page = request.args.get('page', 1, type=int)
    tickets = db.session.query(Flight, Ticket).join("tickets").filter(flight_id == Ticket.flight_id).paginate(page, 9, False)
    tickets_dto = [ticket[1] for ticket in tickets.items]
    next_url = url_for('flight', id=flight_id, page=tickets.next_num) if tickets.has_next else None
    prev_url = url_for('flight', id=flight_id, page=tickets.prev_num) if tickets.has_next else None
    return render_template(
        'flight.html',
        title='Assigned Tickets',
        tickets=tickets_dto,
        next_url=next_url,
        prev_url=prev_url
    )


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
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.state = form.state.data
        current_user.country = form.country.data

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


@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('explore'))
    page = request.args.get('page', 1, type=int)
    flights, total = Flight.search(g.search_form.q.data, page, 6)

    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * 6 else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', flights=flights,
                           next_url=next_url, prev_url=prev_url)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
