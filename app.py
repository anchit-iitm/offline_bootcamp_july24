from flask import Flask, render_template, request, jsonify
from model import db

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
        print(var3["data"])
        # return var3["data"]
        return jsonify({"message": "got the data!", "data": var3["data"]})
    if request.method == "GET":
        var1 = "Hello World from app.py!"
        # return render_template("main.html", var2=var1)
        return jsonify({"var2": var1})

if __name__ == "__main__":
    app.run(debug=True)