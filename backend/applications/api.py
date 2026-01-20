from flask import request, current_app as app
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from .models import db, Users, Category, Products, Cart, Orders, CategoryRequest


class WelcomeAPI(Resource):
    @jwt_required
    def get(self):
        print(get_jwt_identity)
        return {'message': 'Hello, This is GroceryStore!'}, 200
    
    def post(self):
        msg = f'Hello! {request.get_json().get("name")}'
        return {'message':msg}, 200
    


class LoginAPI(Resource):
    def post(self):
        data = request.json

        user = Users.query.filter_by(email=data.get('email')).first()
        if not user:
            return {'message': 'User not found.'}, 404

        if user.password != data.get('password'):
            return {'message': 'Incorrect password.'}, 400

        token = create_access_token(identity=str(user.id))

        return {
            'message': 'User logged in successfully.',
            'token': token,
            'user_name': user.name,
            'user_role': user.role
        }, 200

        
    


class SignupAPI(Resource):
    def post(self):
        data = request.json
        user = Users.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message': 'User already exists'}, 400
        new_user = Users(name=data.get('name'), email=data.get('email'), 
                        password=data.get('password'), role=data.get('role'))
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User signup successfully.'}, 201
        


class CategoryAPI(Resource):

    @jwt_required()
    def get(self):
        categories = Category.query.all()
        category_json = []
        for category in categories:
            # category_json.append({'id': category.id, 'name': category.name})
            category_json.append(category.convert_to_json())
        return category_json, 200


    @jwt_required()
    def post(self):
        data = request.json
        if not data.get('name'):
            return {"message": 'Bad request! all the data fields are required.'}, 400
        
        if len(data.get('name').strip()) > 101 or len(data.get('name').strip()) < 4:
            return {'message': 'Length of name should be in between 4-100 char.'}, 400
        
        new_category = Category(name=data.get('name').strip())
        db.session.add(new_category)
        db.session.commit()
        return {'message': 'Category created successfully.'}, 201
    

    @jwt_required()
    def put(self, category_id):
        data = request.json
        if not data.get('name'):
            return {"message": 'Bad request! all the data fields are required.'}, 400
        
        if len(data.get('name').strip()) > 101 or len(data.get('name').strip()) < 4:
            return {'message': 'Length of name should be in between 4-100 char.'}, 400
        
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found.'}, 404    
        
        category.name = data.get('name').strip()
        db.session.commit()
        return {'message': 'Category updated successfully.'}, 200
    

    @jwt_required()
    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category not found.'}, 404    
        
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully.'}, 200
