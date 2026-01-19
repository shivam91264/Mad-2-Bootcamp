from flask import Flask, request
from flask_restful import Api
from applications.models import db, Users
from applications.api import WelcomeAPI, LoginAPI, SignupAPI
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"


# @app.route('/')
# def home():
#     return 'Hello World!'


db.init_app(app)
api = Api(app)
app.app_context().push()


# def add_admin():
#     admin = Users.query.filter_by(email='admin@gs.com', role = "admin").first()
#     if not admin:
#         admin = Users(name="Admin", email='admin@gs.com', password='2030', role = "admin")
#         db.session.add(admin)
#         db.session.commit()
#         return "Admin added"


api.add_resource(WelcomeAPI, '/api/welcome')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(SignupAPI, '/api/signup')



if __name__ == '__main__':
    db.create_all()
    # add_admin()
    app.run(debug=True)

