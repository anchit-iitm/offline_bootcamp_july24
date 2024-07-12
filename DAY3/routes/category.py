from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, auth_token_required, roles_accepted

from models import db, Category

class Categories(Resource):
    @auth_token_required
    @roles_accepted("admin", "manager")
    def post(self):
        data = request.get_json()
        name = data["name"]
        description = data["description"]
        userid = current_user.id
        check = Category.query.filter_by(name=name).first()
        if not check:
            new_cat = Category(name=name, description=description, user_id=userid)
            db.session.add(new_cat)
            if current_user.has_role("admin"):
                new_cat.status = True
            db.session.commit()
            return make_response(jsonify({"message": "Category is created successfully", "cate_id": new_cat.id}), 201)
        return make_response(jsonify({"message": "Category is already present"}), 409)
    def get(self):
        return "get"
    def put(self):
        data = request.get_json()
        name = data["name"]
        Nname = data["Nname"]
        description = data["description"]
        userid = current_user.id
        cate = Category.query.filter_by(name=name).first()
        if cate:
            cate.name = Nname
            cate.description = description
            cate.user_id = userid
            if current_user.has_role("admin"):
                cate.status = True
            db.session.commit()
            return make_response(jsonify({"message": "Category is uodated successfully", "cate_id": cate.id}), 201)
        return make_response(jsonify({"message": "Category is not present"}), 404)
    
    def delete(self):
        data = request.get_json()
        id = data["id"]
        cate = Category.query.filter_by(id=id).first()
        if cate:
            db.session.delete(cate)
            db.session.commit()    
            return make_response(jsonify({"message": "Category is uodated successfully", "cate_id": cate.id}), 201)
        return make_response(jsonify({"message": "Category is not present"}), 404)