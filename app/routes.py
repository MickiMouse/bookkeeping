import itsdangerous
from app import app, db
from app.forms import LoginForm, RegisterForm, CreateCardForm, ResetPasswordRequest, ResetPassword
from app.models import User, Card
from app.email import send_password_reset, send_request_confirm
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.urls import url_parse
from datetime import datetime


serializer = itsdangerous.URLSafeSerializer(secret_key=app.config['SECRET_KEY'])
ACTIVATION_SALT = 'activate-salt'


@app.route('/')
def preview():
    return render_template('preview.html')


@app.route('/index')
@login_required
def index():
    cards = Card.query.filter_by(payer=current_user).order_by(Card.timestamp.desc())
    return render_template('index.html', cards=cards)


@app.route('/note', methods=['GET', 'POST'])
@login_required
def create_note():
    form = CreateCardForm()
    entries = ['Housing', 'Utilities', 'Food', 'Transport', 'Services', 'Clothes', 'Household',
               'Medicines', 'Credit', 'Technique', 'Entertainment', 'Education', 'Presents']
    if form.validate_on_submit():
        note = Card(price=float(form.price.data),
                    kind=form.kind.data,
                    category=form.category.data,
                    payer=current_user,
                    timestamp=datetime.utcnow())
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('make_note.html', form=form, entries=entries)


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
