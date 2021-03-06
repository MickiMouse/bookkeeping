from app import mail, create_app
from flask_mail import Message
from threading import Thread


def send_async_email(application, msg):
    with application.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients,
                  body=text_body, html=html_body)
    Thread(target=send_async_email, args=(create_app(), msg)).start()
