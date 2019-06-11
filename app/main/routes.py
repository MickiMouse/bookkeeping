import calendar
from datetime import datetime
from app.main import bp
from app.request_db import CardResponse
from app.crendentials import *
from app.models import Card
from flask import render_template, request, current_app
from flask_login import login_required, current_user


@bp.route('/')
def preview():
    return render_template('main/preview.html')


@bp.route('/index', methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)
    year = request.args.get('year', datetime.utcnow().year, type=int)

    if month < 1:
        month = 12
        year = year - 1
    elif month > 12:
        month = 1
        year = year + 1

    cards = Card.query.filter_by(
        payer=current_user,
        month=month,
        year=year
    ).order_by(Card.timestamp.desc()).paginate(
        page=page,
        per_page=current_app.config['CARDS_PER_PAGE'],
        error_out=False)

    date = [calendar.month_name[month], str(year)]

    # statistics
    response = CardResponse(current_user, month=month, year=year)
    categories, prices = response.get_cards('category')
    percents = get_percents(categories, prices)

    # pie
    colors = ['#0260E8', '#64C7FF', '#004156', '#41B619', '#F5E027', '#FB9F82',
              '#FF6B00', '#FFDFDC', '#B40A1B', '#DC3790', '#A400FF', '#58595B']
    bg_colors = colors[:len(categories)]

    all_cards = Card.query.filter_by(payer=current_user,
                                     month=month,
                                     year=year).all()
    total = get_total(all_cards)
    return render_template('main/index.html', cards=cards,
                           date=date, categories=categories, prices=prices, bg_colors=bg_colors, page=page,
                           total=total, percents=percents, month=month, year=year)


@bp.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    cards = current_user.notes.all()
    return render_template('main/table.html', cards=cards)


@bp.route('/describe', methods=['GET'])
@login_required
def describe():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    category = request.args.get('category', type=str)

    date = [calendar.month_name[month], str(year)]

    response = CardResponse(current_user)
    months, prices_months = response.get_expenses_month(year=year, category=category)
    months = calendar_month(months)

    response = CardResponse(current_user, month=month)
    categories, prices_category = response.get_cards('category')

    try:
        idx = categories.index(category)
        target = categories.pop(idx)
        price = prices_category.pop(idx)
        categories = [target, 'Other']
        prices_category = [price, sum(prices_category)]
    except:
        categories = ['Other']
        prices_category = [sum(prices_category)]

    response = CardResponse(current_user, category=category, month=month)
    days, prices_days = response.get_cards('day')

    return render_template('main/stat_expenses.html',
                           date=date, months=months, prices_months=prices_months,
                           categories=categories, prices_category=prices_category,
                           days=days, prices_days=prices_days,
                           month=month, year=year, category=category)


@bp.route('/get_data', methods=['GET'])
@login_required
def get_data():
    _page = request.args.get('page', 1, type=int)
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    cards = Card.query.filter_by(
        payer=current_user,
        month=month,
        year=year
    ).order_by(Card.timestamp.desc()).paginate(
        page=_page,
        per_page=current_app.config['CARDS_PER_PAGE'],
        error_out=False)
    next_url_page = cards.next_num if cards.has_next else None
    prev_url_page = cards.prev_num if cards.has_prev else None
    all_cards = Card.query.filter_by(payer=current_user,
                                     month=month,
                                     year=year).all()
    total = get_total(all_cards)
    return render_template('include/_card.html', cards=cards, _page=_page,
                           ajax_next_url=next_url_page, ajax_prev_url=prev_url_page,
                           total=total)
