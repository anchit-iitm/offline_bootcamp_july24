from flask import request
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

    return app, api

app, api_handler = create_app()

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



if __name__ == "__main__":
    app.run(debug=True)