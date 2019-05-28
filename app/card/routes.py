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
        card = Card(price=form.price.data,
                    category=form.category.data,
                    note=form.note.data,
                    kind=bool(form.kind.data),
                    payer=current_user,
                    year=datetime.utcnow().date().year,
                    month=datetime.utcnow().date().month,
                    day=datetime.utcnow().date().day)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_card.html', form=form)


@bp.route('/change/<id>', methods=['GET', 'POST'])
def change(id):
    card = Card.query.get(int(id))
    form = CardForm()
    if form.validate_on_submit():
        card.kind = form.kind.data
        card.price = form.price.data
        card.category = form.category.data
        card.note = form.note.data
        db.session.commit()
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.kind.data = card.kind
        form.price.data = card.price
        form.category.data = card.category
        form.note.data = card.note
    return render_template('change_card.html', form=form)


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    card = Card.query.get(int(id))
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('main.index'))
