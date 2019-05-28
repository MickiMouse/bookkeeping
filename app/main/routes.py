import calendar
from datetime import datetime
from app.main import bp
from app.graph import Graph
from app.models import Card
from flask import render_template, url_for, request, current_app
from flask_login import login_required, current_user
from crendentials import *


@bp.route('/')
def preview():
    return render_template('preview.html')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    currency = '$'
    page = request.args.get('page', 1, type=int)
    cards = Card.query.filter_by(
        payer=current_user,
        month=datetime.utcnow().month,
        year=datetime.utcnow().year
    ).order_by(Card.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['CARDS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.index', page=cards.next_num) if cards.has_next else None
    prev_url = url_for('main.index', page=cards.prev_num) if cards.has_prev else None

    colors = ['#AB2B52', '#7c1f7C', '#4F2982', '#94002D', '#6C006C', '#330570',
              '#120873', '#689AD3', '#542881', '#2618B1', '#5C0DAC', '#0D56A6']

    chart = Graph(current_user)
    categories, prices = chart.get_cards('category')

    bg_colors = colors[:len(categories)]
    date = '{} {}'.format(calendar.month_name[datetime.utcnow().month], datetime.utcnow().year)

    all_cards = Card.query.filter_by(payer=current_user,
                                     month=datetime.utcnow().month,
                                     year=datetime.utcnow().year).all()
    total = get_total(all_cards)
    percents = get_percents(categories, prices)
    return render_template('index.html', cards=cards, next_url=next_url, prev_url=prev_url,
                           date=date, categories=categories, prices=prices, bg_colors=bg_colors,
                           total=total, percents=percents, currency=currency)


@bp.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    cards = current_user.notes.all()
    return render_template('table.html', cards=cards)


@bp.route('/describe/<category>/<year>', methods=['GET'])
@login_required
def describe(category, year):
    filter_dict = {'category': category, 'year': year}
    chart = Graph(current_user)
    month, prices_mon = chart.get_exp_month(**filter_dict)
    month = calendar_month(month)

    chart = Graph(current_user)
    categories, prices_cat = chart.get_cards('category')

    date = '{} {}'.format(calendar.month_name[datetime.utcnow().month], datetime.utcnow().year)
    return render_template('statistics.html', month=month, prices_mon=prices_mon, category=category,
                           preces_cat=prices_cat, categories=categories, date=date)
