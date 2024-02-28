from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.Signupdb import MyDatabase
import hashlib

blp = Blueprint("Signup", __name__, description="Operations on Signup form")

@blp.route("/Signup")
class Signup(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    def post(self):
        # Access JSON data using request.json
        request_data = request.json
        name =request_data.get("name")
        email = request_data.get("email")
        password = request_data.get("password")
        role = request_data.get("role")

        if role == 'staff':
            result = self.db.signup_staff(name,email, password)
        elif role == 'customer':
            result = self.db.signup_customer(name,email, password)
        else:
            return abort(400, message="Invalid role specified")

        if result:
            return result, 201  # Successfully created
        else:
            return abort(500, message="Error creating user")
          