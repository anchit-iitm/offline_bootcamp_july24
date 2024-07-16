from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                    String, ForeignKey
from flask_security import UserMixin, RoleMixin, AsaList, \
                           SQLAlchemyUserDatastore
from datetime import datetime

db = SQLAlchemy()

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'fs_uniquifier': self.fs_uniquifier,
            'confirmed_at': self.confirmed_at
        }
    
    def get_all_users():
        return User.query.all()
    
    def get_all_managers():
        return User.query.filter_by(role='manager').all()
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    
class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())
    created_by = Column(Integer(), ForeignKey('user.id'))
    updated_by = Column(Integer(), ForeignKey('user.id'))
    status = Column(Boolean(), default=False)
    delete = Column(Boolean(), default=False)
    products = relationship('Product', backref='category', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'delete': self.delete,
            'products': [product.serialize() for product in self.products] if self.products else 'No products found'
        }
    
    def get_all_categories():
        data = Category.query.all()
        if data:
            return data
        return False
    
    def get_category_by_id(id):
        return Category.query.filter_by(id=id).first()
    
    def admin_delete(id):
        category = Category.query.filter_by(id=id).first()
        db.session.delete(category)
        db.session.commit()
        if Category.query.filter_by(id=id).first() == None:
            return True
        return False
    
    def manager_delete(id):
        category = Category.query.filter_by(id=id).first()
        category.delete = True
        db.session.commit()
        if Category.query.filter_by(id=id).first().delete == True:
            return True
        return False


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    price = Column(Integer())
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), onupdate=datetime.now())
    created_by = Column(Integer(), ForeignKey('user.id'))
    updated_by = Column(Integer(), ForeignKey('user.id'))
    status = Column(Boolean(), default=False)
    delete = Column(Boolean(), default=False)
    category_id = Column(Integer(), ForeignKey('category.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'delete': self.delete,
            'category_id': self.category_id
        }
    
    def get_all_products():
        return Product.query.all()
    
    def get_product_by_id(id):
        return Product.query.filter_by(id=id).first()
    
    def admin_delete(id):
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        if Product.query.filter_by(id=id).first() == None:
            return True
        return False
    
    def manager_delete(id):
        product = Product.query.filter_by(id=id).first()
        product.delete = True
        db.session.commit()
        if Product.query.filter_by(id=id).first().delete == True:
            return True
        return False

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    delete = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'delete': self.delete
        }
    
    def get_shopping_cart_by_user_id(user_id):
        return ShoppingCart.query.filter_by(user_id=user_id).all()
    
    def clear_shopping_cart(user_id):
        shopping_cart = ShoppingCart.query.filter_by(user_id=user_id).all()
        for item in shopping_cart:
            db.session.delete(item)
        db.session.commit()
        if ShoppingCart.query.filter_by(user_id=user_id).all() == []:
            return True
        return False
    
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    order_date = db.Column(db.DateTime, default=datetime.now())
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(50), default='Pending')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_date': self.order_date,
            'total_amount': self.total_amount,
            'status': self.status
        }
    
    def get_all_orders():
        return Order.query.all()
    
    def get_order_by_userid(user_id):
        return Order.query.filter_by(user_id=user_id).all()
    
    def get_order_by_id(id):
        return Order.query.filter_by(id=id).first()

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    product_price = db.Column(db.Float)
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product_price': self.product_price
        }
    
    def get_order_items_by_order_id(order_id):
        return OrderItem.query.filter_by(order_id=order_id).all()
    
    def get_order_items_by_product_id(product_id):
        return OrderItem.query.filter_by(product_id=product_id).all()