from flask_mail import Message
from application import mail

def send_email (subject, sender, recepients, txt_body, html_hody):
    msg = Message(subject, sender=sender, recipients=recepients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Sample DataManager] Reset Password',
            sender=app.config['ADMINS'][0],
            recepients=[user.email],
            text_body=render_template('email/reset_password.txt', user=user, token=token),
            html_body=render_template('email/reset_password.html', user=user,token=token)
    )