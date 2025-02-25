# Day2: FLask-Security

from flask import Flask, request, jsonify
from flask_security import Security, verify_password, auth_token_required, roles_accepted, login_user

from models import db, user_datastore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.sqlite3"
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "its_very_secret"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Anchit"
app.config['SECURITY_TRACKABLE'] = True


db.init_app(app)

security = Security(app, user_datastore)

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name="admin", description="Administrator")
    user_datastore.find_or_create_role(name="manager", description="store-manager")
    user_datastore.find_or_create_role(name="customer", description="store-customer")
    db.session.commit()

    admin_user = user_datastore.find_user(email="admin@a.com")
    # admin_user = User.query.filter_by(email="admin@a.com").first()
    
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
    if admin_user:
        user_datastore.add_role_to_user(admin_user, "admin")
        user_datastore.add_role_to_user(admin_user, "manager")
        user_datastore.add_role_to_user(admin_user, "customer")
        db.session.commit()
        if admin_user.has_role("admin"):
            print("Admin user already exists!")


@app.route("/signup", methods=["POST"])
def singup():
    var3 = request.get_json()
    name1 = var3["email"]
    desc = var3["password"]
    username1 = var3["username"] 
    role = var3["role"]   
    print(name1, desc, username1)
    if user_datastore.find_user(email=name1):
        return jsonify({"message": "User already exists!"}), 403
        
    user = user_datastore.create_user(email=name1, 
                                   password=desc, 
                                   username=username1)
    if role == "manager":
        user_datastore.deactivate_user(user)
    user_datastore.add_role_to_user(user, role)
    db.session.commit()
    return jsonify({"message": "Data added!", "id": user.id})

@app.route("/signin", methods=["POST"])
def signin():
    json = request.get_json()
    email = json["email"]
    password = json["password"]

    user = user_datastore.find_user(email=email)
    if user:
        if verify_password(password, user.password):
            token = user.get_auth_token()
            print(user.roles[0].name)
            login_user(user)
            db.session.commit()
            return jsonify({"message": "User found!", "authToken": token, "email": user.email, "role": user.roles[0].name}), 200
        return jsonify({"message": "Invalid password!"}), 403
    

    return jsonify({"message": "User not found!"}), 404
    
@app.route('/test')
@auth_token_required
@roles_accepted("manager")
def test():
    return "Hello World!"

if __name__ == "__main__":
    app.run() 