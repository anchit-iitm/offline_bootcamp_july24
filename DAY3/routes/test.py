from flask_restful import Resource

class test_restful(Resource):
    def post(self):
        return "POST"
    def get(self):
        return "get"
    def put(self):
        return "put"
    def delete(self):
        return "delete"
    