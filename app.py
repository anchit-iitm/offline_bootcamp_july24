#  DAY 1

from flask import Flask, render_template, request, jsonify, make_response

from model import db, User as test, Details

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # var3 = request.form
        var3 = request.get_json()
        name1 = var3["name"]
        desc = var3["data"]
        print(name1, desc)
        result = test.query.filter_by(name=name1).first()
        if not result:
            new_data = test(name=name1, description=desc)
            db.session.add(new_data)
            db.session.commit()
            return jsonify({"message": "Data added!", "id": new_data.id})
        # return var3["data"]
        # return jsonify({"message": "got the data!", "data": result.id})
        result.name = "my name is changed"
        db.session.commit()
        return jsonify({"message": "name already present", "data": result.name}), 409
    

    if request.method == "GET":
        var1 = "Hello World from app.py!"
        data = test.query.all()
        print(data)

        final_data = []

        for i in data:
            print(i.name, i.id, i.description)
            format = {
                "id": i.id,
                "name": i.name,
                "description": i.description
            }
            # print(format)
            
            final_data.append(format)

        # final_data = [i.serialize() for i in data]

        print(final_data)

        # return render_template("main.html", var2=var1)
        # return jsonify({"var2": var1})
        return jsonify({"data": final_data})


@app.route("/getdata", methods=["GET"])
def get_data():
    var3 = request.get_json()
    id1 = var3["id"]
    result = test.query.filter_by(id=id1).first()
    if result:
        return jsonify({"name": result.name, "data": result.id, "decs": result.description})
    return jsonify({"message": "Data not found!"}), 404

@app.route("/post", methods=["POST"])
# rbac
def post():
    if request.method == "POST":
        # var3 = request.form
        var3 = request.get_json()
        email1 = var3["email"]
        add1 = var3["add"]
        id1 = var3["id"]
        print(email1, add1, id)
        check = test.query.filter_by(id=id1).first()
        if check:
            new_details = Details(email=email1, 
                                  address=add1, 
                                  user_id=check.id)  
            db.session.add(new_details)
            db.session.flush()
            # saving pdf and if the pdf is svae then only i will this entry to the table
            db.session.commit()
        # return var3["data"]
        # return jsonify({"message": "got the data!", "data": result.id})
        return jsonify({"message": "name already present", "data": check.name}), 409

if __name__ == "__main__":
    app.run(debug=True)