from app.models import User
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, \
    PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


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
    submit = SubmitField('Register')

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
    kind = SelectField('Kind of card', validators=[DataRequired()],
                       choices=[('Expense', 'Expense'), ('Profit', 'Profit')])
    category = StringField('Category', validators=[DataRequired()])
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
