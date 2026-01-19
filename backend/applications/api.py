from flask import request, current_app as app
from flask_restful import Resource, Api
from .models import db, Users, Category, Products, Cart, Orders, CategoryRequest


class WelcomeAPI(Resource):
    def get(self):
        print(request)
        return {'message': 'Hello, This is GroceryStore!'}, 200
    
    def post(self):
        msg = f'Hello! {request.get_json().get("name")}'
        return {'message':msg}, 200
    


class LoginAPI(Resource):
    def post(self):
        data = request.json
        user = Users.query.filter_by(email=data.get('email')).first()
        if user:
            if user.password == data.get('password'):
                return {'message': 'User logged in successfully.'}, 200
            return {'message': 'Incorrect password.'}, 400
        return {'message': 'User not found.'}, 404
    


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
        