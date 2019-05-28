from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

entries = [('Housing', 'Housing'), ('Utilities', 'Utilities'), ('Food', 'Food'), ('Transport', 'Transport'),
           ('Services', 'Services'), ('Clothes', 'Clothes'), ('Household', 'Household'),
           ('Medicines', 'Medicines'), ('Credit', 'Credit'), ('Technique', 'Technique'),
           ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Other', 'Other')]
kind_choice = [(0, 'Expenses'), (1, 'Income')]


class CreateCardForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=entries, validators=[DataRequired()])
    kind = SelectField(choices=kind_choice, coerce=int)
    note = TextAreaField('Note', validators=[Length(max=32)])
    submit = SubmitField('Create')

    def validate_price(self, price):
        try:
            float(price.data)
        except ValidationError:
            raise ValidationError('Price must be float')
