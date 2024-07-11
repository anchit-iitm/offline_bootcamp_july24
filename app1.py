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
    user_datastore.find_or_create_role(name="admin", description="Administrator")
    user_datastore.find_or_create_role(name="manager", description="store-manager")
    user_datastore.find_or_create_role(name="customer", description="store-customer")
    db.session.commit()

    admin_user = user_datastore.find_user(email="admin@a.com")
    if not admin_user:
        # user_datastore.create_user(email="admin@a.com", 
        #                            password="admin", 
        #                            username="admin", 
        #                            roles=["admin"])
        
        user = user_datastore.create_user(email="admin@a.com", 
                                   password="admin", 
                                   username="admin")
        # user_datastore.add_role_to_user(user, "admin")
        # user_datastore.add_role_to_user(user, "manager")
        # user_datastore.add_role_to_user(user, "customer")
        db.session.commit()
    user_datastore.add_role_to_user(admin_user, "admin")
    user_datastore.add_role_to_user(admin_user, "manager")
    user_datastore.add_role_to_user(admin_user, "customer")
    db.session.commit()
    

if __name__ == "__main__":
    app.run() 