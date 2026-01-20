from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey
from datetime import datetime


# User Table, Category Table, Product Table, Cart Table
# Order Table, CategoryRequest Table
# User: Manager Table, Customer Table, Admin Table



db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    name = Column(String(60), nullable=False)
    role = Column(String(10), nullable=False, default="customer")
    status = Column(String(20), unique=False, default="active")

    carts = db.relationship('Cart', backref='users', cascade="all, delete-orphan", lazy=True)
    category_requests = db.relationship('CategoryRequest', backref='users', lazy=True)



class Category(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    products = db.relationship('Products', backref='category', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<category {self.name!r}>'
    
    def convert_to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }



class Products(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    unit = Column(String(20), nullable=False)
    stock = Column(Integer, nullable=False)
    sold = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    carts = db.relationship('Cart', backref='products', cascade="all, delete-orphan", lazy=True)


    def convert_to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "unit": self.unit,
            "stock": self.stock,
            "sold": self.sold,
            "category_id": self.category_id,
            "category_name": self.category_name
        }






class Cart(db.Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id') , nullable=False)
    customer_id = Column(Integer, ForeignKey('users.id') , nullable=False)


class Orders(db.Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    date_of_purchase = Column(String(20), default=datetime.now(), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id') , nullable=False)
    customer_id = Column(Integer, ForeignKey('users.id') , nullable=False)



class CategoryRequest(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    category_id = Column(Integer, nullable=True)
    action = Column(String(10), nullable=False)

    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
