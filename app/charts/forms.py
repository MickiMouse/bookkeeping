from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

year_choices = [(2019, 2019)]
month_choise = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
                ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]

entries = [('Housing', 'Housing'), ('Utilities', 'Utilities'), ('Food', 'Food'), ('Transport', 'Transport'),
           ('Services', 'Services'), ('Clothes', 'Clothes'), ('Household', 'Household'),
           ('Medicines', 'Medicines'), ('Credit', 'Credit'), ('Technique', 'Technique'),
           ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Other', 'Other')]


class CreateCardForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=entries, validators=[DataRequired()])
    note = TextAreaField('Note', validators=[Length(max=32)])
    submit = SubmitField('Create')

    def validate_price(self, price):
        try:
            float(price.data)
        except ValidationError:
            raise ValidationError('Price must be float')


class DaysLineForm(FlaskForm):
    month_days = SelectField('Month', choices=month_choise, coerce=str, validators=[DataRequired()])
    year_days = SelectField('Year', choices=year_choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Show')


class MonthCategoryForm(FlaskForm):
    month_category = SelectField('Month', choices=month_choise, coerce=str, validators=[DataRequired()])
    year_category = SelectField('Year', choices=year_choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Show')


class CategoryForm(FlaskForm):
    category = SelectField('Category', choices=entries, validators=[DataRequired()])
    year = SelectField('Year', choices=year_choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Show')


class MonthLineForm(FlaskForm):
    year_line = SelectField('Year', choices=year_choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Show')


class CategoryMonthForm(FlaskForm):
    month = SelectField('Month', choices=month_choise, coerce=str, validators=[DataRequired()])
    category = SelectField('Category', choices=entries, validators=[DataRequired()])
    year_category = SelectField('Year', choices=year_choices, coerce=int, validators=[DataRequired()])
    submit = SubmitField('Show')
