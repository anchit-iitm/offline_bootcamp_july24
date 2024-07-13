from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted
from models import db, user_datastore, Product, Category

class switch_manager(Resource):
    @auth_token_required
    @roles_accepted("admin")
    def post(self):
        data = request.get_json()
        manager = user_datastore.find_user(id=data['id'])
        if manager and manager.roles[0].name == "manager":
            if manager.active:
                user_datastore.deactivate_user(manager)
            user_datastore.activate_user(manager)
            db.session.commit()
            return make_response(jsonify({"message": "manager activated", "email": manager.email, "id": manager.id, "status": manager.active}), 200)
        return make_response(jsonify({"message": "manager not found", "email": manager.email}), 404)
    
class switch_product(Resource):
    def post(self):
        data = request.get_json()
        product = Product.query.filter_by(id=data['id']).first()
        if product:
            if product.status:
                product.status = False
            else:
                product.status = True
            db.session.commit()
            return make_response(jsonify({"message": "product deleted", "id": product.id, "status": product.delete}), 200)
        return make_response(jsonify({"message": "product not found", "id": product.id}), 404)
    
class switch_category(Resource):
    def post(self):
        data = request.get_json()
        category = Category.query.filter_by(id=data['id']).first()
        if category:
            if category.delete:
                category.delete = False
            else:
                category.delete = True
            db.session.commit()
            return make_response(jsonify({"message": "category deleted", "id": category.id, "status": category.delete}), 200)
        return make_response(jsonify({"message": "category not found", "id": category.id}), 404)
    

