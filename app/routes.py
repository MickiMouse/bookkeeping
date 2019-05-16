import calendar
import itsdangerous
from app import app, db
from app.forms import *
from app.models import User, Card
from app.email import send_password_reset, send_request_confirm
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.urls import url_parse
from datetime import datetime
from app.graph import Graph


serializer = itsdangerous.URLSafeSerializer(secret_key=app.config['SECRET_KEY'])
ACTIVATION_SALT = 'activate-salt'


@app.route('/')
def preview():
    return render_template('preview.html')


@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    cards = Card.query.filter_by(payer=current_user).order_by(Card.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['CARDS_PER_PAGE'],
        error_out=False)
    print(cards.items)
    next_url = url_for('index', page=cards.next_num) if cards.has_next else None
    prev_url = url_for('index', page=cards.prev_num) if cards.has_prev else None
    return render_template('index.html', cards=cards, next_url=next_url, prev_url=prev_url)


@app.route('/note', methods=['GET', 'POST'])
@login_required
def create_card():
    form = CreateCardForm()
    entries = [('Housing', 'Housing'), ('Utilities', 'Utilities'), ('Food', 'Food'), ('Transport', 'Transport'),
               ('Services', 'Services'), ('Clothes', 'Clothes'), ('Household', 'Household'),
               ('Medicines', 'Medicines'), ('Credit', 'Credit'), ('Technique', 'Technique'),
               ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Other', 'Other')]
    form.category.choices = entries
    if form.validate_on_submit():
        card = Card(price=float(form.price.data),
                    category=form.category.data,
                    note=form.note.data,
                    payer=current_user,
                    year=datetime.utcnow().date().year,
                    month=datetime.utcnow().date().month,
                    day=datetime.utcnow().date().day)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_card.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Wrong email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        token = serializer.dumps(user.as_dict(), salt=ACTIVATION_SALT)
        send_request_confirm(user, token)
        flash('Check your email and confirm your account')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset(user)
            flash('Check your email')
            return redirect(url_for('login'))
        else:
            flash('Sorry, we have not user with this email')
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.set_password(form.password2.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    cards = current_user.notes.all()
    return render_template('table.html', cards=cards)


@app.route('/confirm/<token>')
def confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    try:
        user_dict = serializer.loads(token, salt=ACTIVATION_SALT)
        user = User(email=user_dict['email'],
                    username=user_dict['username'],
                    pass_hash=user_dict['pass_hash'])
        db.session.add(user)
        db.session.commit()
        flash('Account has been confirmed')
    except itsdangerous.BadSignature:
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
    form_day = ChooseMonthForm()
    form_cat = CategoryForm()
    if form_day.validate_on_submit():
        return redirect(url_for('graph_days', month=form_day.month.data, year=form_day.year.data))
    if form_cat.validate_on_submit():
        return redirect(url_for('graph_cat', month=form_cat.month.data))
    return render_template('graph.html', form_day=form_day, form_cat=form_cat)


@app.route('/days-<month>-<year>', methods=['GET', 'POST'])
@login_required
def graph_days(month, year):
    plot = Graph(current_user)
    days, prices = plot.get_data_plot_days(int(month), year)
    return render_template('graph_days.html', days=days, prices=prices, month=calendar.month_name[int(month)])


@app.route('/categories-<month>', methods=['GET', 'POST'])
@login_required
def graph_cat(month):
    plot = Graph(current_user)
    cat, prices = plot.get_data_plot_cat(int(month))
    return render_template('graph_categories.html', cat=cat, prices=prices, month=calendar.month_name[int(month)])


@app.route('/stat', methods=['GET', 'POST'])
@login_required
def stat():
    pass
