from datetime import datetime
from app import db
from app.main import bp
from app.main.forms import CreateCardForm
from app.graph import Graph
from app.models import Card
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user


@bp.route('/')
def preview():
    return render_template('preview.html')


@bp.route('/index')
@login_required
def index():
    # page = request.args.get('page', 1, type=int)
    # cards = Card.query.filter_by(payer=current_user).order_by(Card.timestamp.desc()).paginate(
    #     page=page,
    #     per_page=app.config['CARDS_PER_PAGE'],
    #     error_out=False)
    # next_url = url_for('index', page=cards.next_num) if cards.has_next else None
    # prev_url = url_for('index', page=cards.prev_num) if cards.has_prev else None
    chart = Graph(current_user)
    categories, expenses = chart.get_all_categories()
    return render_template('index.html', categories=categories, expenses=expenses)
    # cards=cards, next_url=next_url, prev_url=prev_url)


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
