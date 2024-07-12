# Day2: FLask-Security

from flask import Flask, request, jsonify
from flask_security import Security, verify_password, auth_token_required, roles_accepted, login_user
from flask_restful import Api

from models import db, user_datastore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.sqlite3"
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "its_very_secret"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Anchit"
app.config['SECURITY_TRACKABLE'] = True


db.init_app(app)
api = Api(app)

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


# @app.route("/signin", methods=["POST"])
# def signin():
#     json = request.get_json()
#     email = json["email"]
#     password = json["password"]

#     user = user_datastore.find_user(email=email)
#     if user:
#         if verify_password(password, user.password):
#             token = user.get_auth_token()
#             print(user.roles[0].name)
#             login_user(user)
#             db.session.commit()
#             return jsonify({"message": "User found!", "authToken": token, "email": user.email, "role": user.roles[0].name}), 200
#         return jsonify({"message": "Invalid password!"}), 403
    

    # return jsonify({"message": "User not found!"}), 404
    
@app.route('/test', methods=["GET", "POST", "PUT", "DELETE"])
# @auth_token_required
# @roles_accepted("manager")
def test():
    if request.method == "POST":
        return "Hello World!, POST"
    if request.method == "GET":
        return "Hello World!, GET" 
    if request.method == "PUT":
        return "Hello World!, PUT" 
    if request.method == "DELETE":
        return "Hello World!, DELETE"  

from routes.test import test_restful
api.add_resource(test_restful, "/api/test")

from routes.auth import signup, login
api.add_resource(signup, "/signup")
api.add_resource(login, "/signin")




if __name__ == "__main__":
    app.run() 