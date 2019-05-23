# import itsdangerous
from app import db
from app.auth import bp
from app.auth.forms import *
from flask import request, redirect, render_template, url_for, flash
from flask_login import current_user, logout_user, login_user
from app.auth.email import send_password_reset
from werkzeug.urls import url_parse

# serializer = itsdangerous.URLSafeSerializer(secret_key=current_app.config['SECRET_KEY'])
# ACTIVATION_SALT = 'activate-salt'


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Wrong email or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data)
        user.set_password(form.password2.data)
        db.session.add(user)
        db.session.commit()
        # token = serializer.dumps(user.as_dict(), salt=ACTIVATION_SALT)
        # send_request_confirm(user, token)
        # flash('Check your email and confirm your account')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset(user)
            flash('Check your email')
            return redirect(url_for('auth.login'))
        else:
            flash('Sorry, we have not user with this email')
    return render_template('reset_password_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user.set_password(form.password2.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


'''
@bp.route('/confirm/<token>')
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
'''