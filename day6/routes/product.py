from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_security import current_user, auth_token_required, roles_accepted

from models import db, Product, Category
from cacher import cache

class Products(Resource):
    @auth_token_required
    @roles_accepted("admin", "manager")
    def post(self):
        # data = request.get_json()
        data = request.form
        name = data["name"]
        description = data["description"]
        price = data["price"]
        category_id = data["category_id"]
        userid = current_user.id
        print(name, description, price, category_id, userid)

        image = request.files["img"]
        print(image)

        import os
        # basedir = os.path.abspath(os.path.dirname(__file__))
        from models import basedir
        print(basedir)


        check = Product.query.filter_by(name=name).first()
        if not check:
            new_product = Product(name=name, description=description, price=price, category_id=category_id, created_by=userid)
            db.session.add(new_product)
            if current_user.has_role("admin"):
                new_product.status = True
            db.session.commit()
            filename = f"{new_product.id}.pdf"
            final_name = os.path.join(basedir, "assests", filename)
            image.save(final_name)
            return make_response(jsonify({"message": "Product is created successfully", "product_id": new_product.id}), 201)
        return make_response(jsonify({"message": "Product is already present"}), 409)
    
    @auth_token_required
    @cache.cached()
    def get(self):
        data = Product.get_all_products()
        if data:
            final_data = []
            for i in data:
                final_data.append(i.serialize())
            return make_response(jsonify({"data": final_data}), 200)
        return make_response(jsonify({"message": "No Product found"}), 404)