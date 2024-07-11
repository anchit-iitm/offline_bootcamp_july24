# Day2: FLask-Security

from flask import Flask
from flask_security import Security

from models import db, user_datastore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.sqlite3"
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "its_very_secret"

db.init_app(app)

security = Security(app, user_datastore)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run() 