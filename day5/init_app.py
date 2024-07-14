from app import create_app
from models import db, user_datastore

app, _ = create_app()

def create_empty_tables():
    db.drop_all()
    db.create_all()

with app.app_context():
    create_empty_tables()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='manager', description='Manager')
    user_datastore.find_or_create_role(name='customer', description='Customer')
    db.session.commit()

    if not user_datastore.find_user(email="admin@a.com"):
        admin_user=user_datastore.create_user(email="admin@a.com", password="admin", username="admin")
        user_datastore.add_role_to_user(admin_user, "admin")

    if not user_datastore.find_user(email="manager@a.com"):
        admin_user=user_datastore.create_user(email="manager@a.com", password="manager", username="manager")
        user_datastore.add_role_to_user(admin_user, "manager")
        user_datastore.deactivate_user(admin_user)

    if not user_datastore.find_user(email="customer@a.com"):
        admin_user=user_datastore.create_user(email="customer@a.com", password="customer", username="customer")
        user_datastore.add_role_to_user(admin_user, "customer")

    db.session.commit()
        
