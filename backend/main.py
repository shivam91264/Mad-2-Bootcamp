from flask import Flask, request
from applications.models import db
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "database.sqlite3")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"


# @app.route('/')
# def home():
#     return 'Hello World!'


db.init_app(app)
app.app_context().push()


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

