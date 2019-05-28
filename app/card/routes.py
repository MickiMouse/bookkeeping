from datetime import datetime
from app import db
from app.card import bp
from app.card.forms import CreateCardForm
from app.models import Card
from flask import redirect, url_for, render_template
from flask_login import login_required, current_user


@bp.route('/add_card', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCardForm()
    if form.validate_on_submit():
        card = Card(price=float(form.price.data),
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


@bp.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    card = Card.query.get(int(id))
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('main.index'))
