from app import mail
from flask_mail import Message
from threading import Thread
from flask import current_app


# 发送异步邮件
def send_async_email(subject, recvs, body, html):
    msg = Message(subject=subject, recipients=recvs, body=body, html=html)
    msg.sender = current_app.config['MAIL_USERNAME']
    app = current_app._get_current_object()
    thead = Thread(target=send_email, args=[app, msg])
    thead.start()

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)
