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


def _calendar_month(args):
    return [calendar.month_name[i] for i in args]


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
    next_url = url_for('index', page=cards.next_num) if cards.has_next else None
    prev_url = url_for('index', page=cards.prev_num) if cards.has_prev else None
    return render_template('index.html', cards=cards, next_url=next_url, prev_url=prev_url)


@app.route('/add_card', methods=['GET', 'POST'])
@login_required
def create_card():
    form = CreateCardForm()
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
    forms = [DaysLineForm(), MonthCategoryForm(), CategoryForm(), MonthLineForm(), CategoryMonthForm()]

    forms_dict = {
        forms[0]: ('graph_days_line', {
            'month': forms[0].month_days.data,
            'year': forms[0].year_days.data
        }),
        forms[1]: ('graph_category_bar', {
            'month': forms[1].month_category.data,
            'year': forms[1].year_category.data
        }),
        forms[2]: ('graph_month_hbar', {
            'category': forms[2].category.data,
            'year': forms[2].year.data
        }),
        forms[3]: ('graph_month_line', {
            'year': forms[3].year_line.data
        }),
        forms[4]: ('graph_category_month', {
            'category': forms[4].category.data,
            'month': forms[4].month.data,
            'year': forms[4].year_category.data
        })
    }

    for form in list(forms_dict.keys()):
        if form.validate_on_submit():
            return redirect(url_for(forms_dict[form][0], **forms_dict[form][1]))

    return render_template('graph.html',
                           form1=forms[0], form2=forms[1], form3=forms[2],
                           form4=forms[3], form5=forms[4])


@app.route('/days/<month>/<year>', methods=['GET'])
@login_required
def graph_days_line(month, year):
    chart = Graph(current_user)
    filter_dict = {'month': int(month), 'year': year}
    days, prices = chart.days(**filter_dict)
    return render_template('graph_days_line.html', days=days, prices=prices, month=_calendar_month([int(month)]))


@app.route('/month/<year>', methods=['GET'])
@login_required
def graph_month_line(year):
    chart = Graph(current_user)
    month, prices = chart.month(year)
    month = _calendar_month(month)
    return render_template('graph_month_line.html', month=month, prices=prices)


@app.route('/categories/<month>/<year>', methods=['GET'])
@login_required
def graph_category_bar(month, year):
    chart = Graph(current_user)
    categories, prices = chart.categories(int(month), year)
    return render_template('graph_categories_bar.html', cat=categories, prices=prices, month=_calendar_month([int(month)]))


@app.route('/category/<category>/<year>', methods=['GET'])
@login_required
def graph_month_hbar(category, year):
    chart = Graph(current_user)
    month, prices = chart.category_per_month(category, year)
    month = _calendar_month(month)
    return render_template('graph_categories_hbar.html', month=month, prices=prices, category=category)


@app.route('/<category>/<month>/<year>', methods=['GET'])
def graph_category_month(category, month, year):
    chart = Graph(current_user)
    filter_dict = {'category': category, 'month': month, 'year': year}
    days, prices = chart.category_per_day(**filter_dict)
    return render_template('graph_category_per_day.html', days=days, prices=prices, category=category)
