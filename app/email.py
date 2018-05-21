from flask_mail import Mail, Message
from threading import Thread
from . import render_template, mail, main


def send_mail(to, subject, template, **kwargs):
    msg = Message(main.app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=main.app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[main.app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
