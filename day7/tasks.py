from app import celery_app
from mailer import mail as email
from taskcontext import ContextTask

@celery_app.task(base=ContextTask)
def test():
    return "x"

@celery_app.task(base=ContextTask)
def mail():
    from models import db, User
    from flask_mail import Message
    email_subject = "Test Email"
    email_body = "This is a test email"
    users = User.query.all()
    for user in users:
        print(user.email)
        format = "<html><body>"
        format += "<h1>Hi, " + user.username + "</h1>"
        format += "<p>" + email_body + "</p>"
        format += "</body></html>"
        msg = Message(subject=email_subject, recipients=[user.email])
        msg.body = email_body
        msg.html = format
        email.send(msg)
    return 'ok'