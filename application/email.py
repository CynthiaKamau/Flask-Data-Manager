from flask_mail import Message
from application import mail, app
from threading import Thread
from flask import render_template
from flask_babel import lazy_gettext

def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

def send_email (subject, sender, recepients, txt_body, html_body):
    msg = Message(subject, sender=sender, recipients=recepients)
    msg.body = txt_body
    msg.html = html_body
    mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(lazy_gettext('[Sample DataManager] Reset Password'),
            sender=app.config['ADMINS'][0],
            recepients=[user.email],
            txt_body=render_template('email/resetpassword.txt', user=user, token=token),
            html_body=render_template('email/resetpassword.html', user=user,token=token)
    )