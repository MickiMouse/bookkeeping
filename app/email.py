from app import app
from app import mail
from flask import render_template
from flask_mail import Message


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients,
                  body=text_body, html=html_body)
    mail.send(msg)


def send_password_reset(user):
    token = user.create_token()
    send_email(subject='Reset Your password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', token=token, user=user),
               html_body=render_template('email/reset_password.html', token=token, user=user))


def send_request_confirm(user, token):
    send_email(subject='Confirm your account',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_user.txt', token=token, user=user),
               html_body=render_template('email/confirm_user.html', token=token, user=user))
