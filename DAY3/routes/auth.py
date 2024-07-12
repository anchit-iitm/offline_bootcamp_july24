from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import verify_password, login_user

from models import user_datastore, db


class signup(Resource):
    def post(self):
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




# @app.route("/signup", methods=["POST"])
# def singup():
#     var3 = request.get_json()
#     name1 = var3["email"]
#     desc = var3["password"]
#     username1 = var3["username"] 
#     role = var3["role"]   
#     print(name1, desc, username1)
#     if user_datastore.find_user(email=name1):
#         return jsonify({"message": "User already exists!"}), 403
        
#     user = user_datastore.create_user(email=name1, 
#                                    password=desc, 
#                                    username=username1)
#     if role == "manager":
#         user_datastore.deactivate_user(user)
#     user_datastore.add_role_to_user(user, role)
#     db.session.commit()
#     return jsonify({"message": "Data added!", "id": user.id})


class login(Resource):
    def post(self):
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
                return make_response(jsonify({"message": "User found!", "authToken": token, "email": user.email, "role": user.roles[0].name}), 900)
            return make_response(jsonify({"message": "Invalid password!"}), 403)