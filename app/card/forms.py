from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, SelectField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError

expenses = [('Housing', 'Housing'), ('Utilities', 'Utilities'), ('Food', 'Food'), ('Transport', 'Transport'),
            ('Services', 'Services'), ('Clothes', 'Clothes'), ('Household', 'Household'),
            ('Medicines', 'Medicines'), ('Credit', 'Credit'), ('Technique', 'Technique'),
            ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Other expenses', 'Other expenses')]
incomes = [('Business', 'Business'), ('Work', 'Work'), ('Other incomes', 'Other incomes')]
kind_choice = [(0, 'Expenses'), (1, 'Income')]


class CardForm(FlaskForm):
    price = FloatField('Price', validators=[DataRequired()])
    category_expenses = SelectField('Category expenses', choices=expenses, coerce=str, validators=[Optional()])
    category_incomes = SelectField('Category incomes', choices=incomes, coerce=str, validators=[Optional()])
    kind = SelectField(choices=kind_choice, coerce=int)
    day = IntegerField(validators=[NumberRange(min=1, max=31)])
    month = IntegerField(validators=[NumberRange(min=1, max=12)])
    year = IntegerField(validators=[NumberRange(min=1970)])
    note = TextAreaField(validators=[Length(max=32)])
    submit = SubmitField('Create')

    def validate_price(self, price):
        try:
            float(price.data)
        except ValidationError:
            raise ValidationError('Price must be float')
