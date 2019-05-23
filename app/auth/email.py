from flask import render_template, current_app
from app.email import send_email


def send_password_reset(user):
    token = user.create_token()
    send_email(subject='Reset Your password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', token=token, user=user),
               html_body=render_template('email/reset_password.html', token=token, user=user))


'''
def send_request_confirm(user, token):
    send_email(subject='Confirm your account',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_user.txt', token=token, user=user),
               html_body=render_template('email/confirm_user.html', token=token, user=user))
'''