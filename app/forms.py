from app.models import User
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, \
    PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

year_choices = [(2019, 2019)]
month_choise = [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
                ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')]

entries = [('Housing', 'Housing'), ('Utilities', 'Utilities'), ('Food', 'Food'), ('Transport', 'Transport'),
           ('Services', 'Services'), ('Clothes', 'Clothes'), ('Household', 'Household'),
           ('Medicines', 'Medicines'), ('Credit', 'Credit'), ('Technique', 'Technique'),
           ('Entertainment', 'Entertainment'), ('Education', 'Education'), ('Other', 'Other')]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use another username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use another email')


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


class ResetPasswordRequest(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset password')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')


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
