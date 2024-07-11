from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): # this is the user table for me as of now
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(100))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
class Details(db.Model):
    __tablename__ = "details"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
