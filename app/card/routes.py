from datetime import datetime
from app import db
from app.card import bp
from app.card.forms import CardForm
from app.models import Card
from flask import request, redirect, url_for, render_template
from flask_login import login_required, current_user


@bp.route('/make_card', methods=['GET', 'POST'])
@login_required
def create():
    form = CardForm()
    if form.validate_on_submit():
        category = form.category_expenses.data if form.kind.data == 0 else form.category_incomes.data
        card = Card(price=form.price.data,
                    category=category,
                    note=form.note.data,
                    kind=bool(form.kind.data),
                    payer=current_user,
                    year=form.year.data,
                    month=form.month.data,
                    day=form.day.data)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.day.data = datetime.utcnow().date().day
        form.month.data = datetime.utcnow().date().month
        form.year.data = datetime.utcnow().date().year
    return render_template('card/create_card.html', form=form)


@bp.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    id = request.args.get('id', type=int)
    card = Card.query.get(int(id))
    form = CardForm()
    if form.validate_on_submit():
        category = form.category_expenses.data if form.kind.data == 0 else form.category_incomes.data
        card.kind = form.kind.data
        card.price = form.price.data
        card.category = category
        card.day = form.day.data
        card.month = form.month.data
        card.year = form.year.data
        card.note = form.note.data
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.kind.data = card.kind
        form.price.data = card.price
        form.category_expenses.data = card.category
        form.category_incomes.data = card.category
        form.day.data = card.day
        form.month.data = card.month
        form.year.data = card.year
        form.note.data = card.note
    return render_template('card/change_card.html', form=form)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    card = Card.query.get(int(id))
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('main.index'))
