import calendar
from datetime import datetime
from app import db
from app.main import bp
from app.main.forms import CreateCardForm
from app.graph import Graph
from app.models import Card
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user


@bp.route('/')
def preview():
    return render_template('preview.html')


@bp.route('/index')
@login_required
def index():
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
    categories, prices = chart.get_all_categories()
    bg_colors = colors[:len(categories)]
    date = '{} {}'.format(calendar.month_name[datetime.utcnow().month], datetime.utcnow().year)
    total = get_total(datetime.utcnow().month, datetime.utcnow().year)
    data = get_percents(categories, prices)
    return render_template('index.html', cards=cards, next_url=next_url, prev_url=prev_url,
                           date=date, categories=categories, prices=prices, bg_colors=bg_colors,
                           total=total, data=data)


@bp.route('/add_card', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template('create_card.html', form=form)


@bp.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    cards = current_user.notes.all()
    return render_template('table.html', cards=cards)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    card = Card.query.get(int(id))
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('main.index'))


def get_percents(categories, prices):
    percents = [x / sum(prices) * 100 for x in prices]
    z = [j for i, j in sorted(zip(percents, categories), key=lambda pair: pair[0])]
    percents.sort()
    percents.reverse()
    z.reverse()
    data = ['{}% {}'.format(round(percents[i], 2), z[i]) for i in range(len(percents))]

    if len(data) > 3:
        return data[:3]
    else:
        return data


def get_total(month, year):
    return sum([card.price for card in Card.query.filter_by(payer=current_user, month=month, year=year).all()])
