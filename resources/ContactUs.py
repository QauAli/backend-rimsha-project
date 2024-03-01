from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from resources.schemas  import ContactUsSchema
from resources.ContactUsdb import MyDatabase

blp = Blueprint("contactUs", __name__, description="Contact-Us form submission")



@blp.route("/contact_us")
class Contact(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    @blp.arguments(ContactUsSchema)
    def post(self,request_data):
        # request_data = request.json
        print("Request Data:", request_data)  # sending JSON data
        if not request_data:
            return abort(400, message="No JSON data provided")
        FirstName = request_data.get("FirstName")
        LastName = request_data.get("LastName")
        Email_id = request_data.get("Email_id")
        Message = request_data.get("Message")
        if not all([FirstName, LastName, Email_id, Message]):
            return abort(400, message="Incomplete form data")

        result = self.db.add_Contactform(FirstName, LastName,Email_id, Message)

        if result:
            return result, 200
        else:
            return abort(500, message="Error processing the form")