from flask import request
from mailer import mail as email

def make_celery(server):
    from celery import Celery
    celery = Celery(server.import_name)
    celery.config_from_object('celeryconfig')
    return celery

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config.from_object("config.localDev")

    from models import db, user_datastore

    db.init_app(app)
    
    from flask_security import Security
    security = Security(app, user_datastore)

    from flask_restful import Api
    api = Api(app)

    from flask_cors import CORS
    CORS(app)

    from cacher import cache
    cache.init_app(app)

    celeryService = make_celery(app)

    email.init_app(app)

    return app, api, celeryService

app, api_handler, celery_app = create_app()

import tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    "test": {
        "task": "tasks.test",
        "schedule": crontab(hour="16", minute="04")
    },
    "mail": {
        "task": "tasks.mail",
        "schedule": crontab(hour="17", minute="19", day_of_month="16")
}
}

@app.route('/mail')
def mail():
    from flask_mail import Message
    email_subject = "Test Email"
    email_body = "This is a test email"

    msg = Message(subject=email_subject, recipients=["kamakotti@iitm.ac.in"])
    msg.body = email_body
    email.send(msg)
    return 'ok'
    

@app.route("/hello_world")
def hello_world():
    return "Hello World!"
from routes.testRest import restTest  
api_handler.add_resource(restTest, "/test")

from routes.auth import login, register
api_handler.add_resource(login, "/api/login")
api_handler.add_resource(register, "/api/register")

from routes.category import Categories, specificCategory
api_handler.add_resource(Categories, "/api/category")
api_handler.add_resource(specificCategory, "/api/category/<int:id>")

from routes.product import Products
api_handler.add_resource(Products, "/api/product")

from routes.admin import switch_manager, switch_product, switch_category
api_handler.add_resource(switch_manager, "/api/switch_manager")

@app.route('/test_celery')
def test_celery():
    from flask import jsonify, make_response
    result = tasks.test.delay()
    while not result.ready():
        pass
    return make_response(jsonify({"task_id": result.id, "task_result": result.status}), 202)

if __name__ == "__main__":
    app.run(debug=True)