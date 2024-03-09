from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os
from flask import jsonify
from werkzeug.utils import secure_filename
from resources.schemas  import CustomerSchema
from resources.schemas  import LoginSchema
from resources.schemas  import CustomerUpdateSchema
from resources.schemas  import ProfileUpdateSchema
from resources.Customerdb import MyDatabase
import hashlib
import json

UPLOAD_FOLDER = 'C:/xampp/htdocs/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



blp = Blueprint("customer", __name__, description="Operations on customer")



@blp.route("/login")
class Login(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    @blp.arguments(LoginSchema)
    def post(self, request_data):
          email = request_data.get("email")
          password = request_data.get("password")
          role = request_data.get("role")
          result= self.db.verify_user(email,password,role)
          if result:
              return result, 200
          else:
           return abort(404, message="Record doesn't exist")
          

@blp.route("/ImageUpload")
class ImageUpload(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    def post(self):
        email = request.form.get("email")
        role = request.form.get("role")

        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Call the upload_profile_image function
            if self.db.upload_profile_image(email, file_path, role):
                return jsonify({"message": "Image uploaded and profile updated successfully"}), 200
            else:
                return jsonify({"message": "Error updating profile"}), 500

        return jsonify({"message": "Invalid file extension"}), 400

          


@blp.route("/ProfileUpdate")
class Profile(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    @blp.arguments(ProfileUpdateSchema)
    def put(self, request_data):
    # Remove the 'id' parameter as it is not needed
     fields = {
        'name': request_data.get('name'),
        'password': request_data.get('password'),
        'email': request_data.get('email'),
        'newpassword': request_data.get('newpassword'),
    }
     print(fields)

     result = self.db.update_profile(body=fields)  # Remove 'id' parameter
     print("update function call")

     if result:
      return {"message": "Record updated successfully"}, 200
     else:
        return abort(404, message="Record doesn't exist")





@blp.route("/customer")
class Customer(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     customers = self.db.view_customer()
     Customer_id = request.args.get("Customer_id")

     if Customer_id is None:
        return customers
     else:
        # Find the customer with the specified ID
        customer = next((c for c in customers if c["Customer_id"] == int(Customer_id)), None)

        if customer is None:
            abort(404, message="Record doesn't exist")

        return customer

     
     


    def get(self):
        Customer_id = request.args.get("Customer_id")
        if Customer_id is None:
            return self.db.get_customers()
        else:
            customer = self.db.get_customer(Customer_id)
            # print(customer)
            if customer is None:
                abort(404, message="Record doesn't exist")
            return customer
        

    # post is use for adding the data
    @blp.arguments(CustomerSchema)
    def post(self, request_data):
        C_Email_Id = request_data.get('C_Email_Id')
        Password = hashlib.sha256(request_data.get("Password").encode('utf-8')).hexdigest()
        C_FirstName = request_data.get('C_FirstName')

        # Check if the customer already exists based on email and first name
        if not self.db.customer_exists(C_Email_Id, C_FirstName):
            self.db.add_customer(C_Email_Id, Password, C_FirstName)
            return {'message': "Customer added successfully"}, 201
        else:
            abort(403, message="Customer already exists")



    # put is used for updating the data
    @blp.arguments(CustomerUpdateSchema)
    def put(self, request_data):
        C_Email_Id = request_data.get('C_Email_Id')
        print(f"Received request with ID: {C_Email_Id}")
        # id = args.get('id')
        if self.db.update_customer(C_Email_Id, request_data):
            return {'message': "customer updated successfully"}, 201
        abort(404, "customer not found")



# @blp.route('/customer', methods=['DELETE'])

    def delete(self):
        Customer_id = request.args.get('Customer_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_customer(Customer_id):
            return {"message": "customer deleted successfully"}
        abort(404, "customer not found")



@blp.route("/total_customers")
class TotalCustomers(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    def get(self):
        total_customers = self.db.get_total_customers()
        response = {"total_customers": total_customers}
        return response



@blp.route("/feedback")
class Feedback(MethodView):
    def __init__(self):
        self.db = MyDatabase()
# put is used because it updates the existing customer email feedback as i use post it posts same id feedback in the same table
    def put(self):
        request_data = request.get_json()
        C_Email_Id = request_data.get('C_Email_Id')
        Feedback = request_data.get('Feedback')

        # Check if the customer already exists based on email
        if self.db.check_customer(C_Email_Id):
            self.db.update_feedback(C_Email_Id, Feedback)
            return {'message': "Feedback send successfully, thanks for your feedback"}, 201
        else:
            return {'error': "Customer does not exist"}, 404
        

@blp.route("/total_feedbacks")
class TotalFeedbacks(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    def get(self):
        customers_with_feedback = self.db.get_customers_with_feedback()
        response = {"customers_with_feedback": customers_with_feedback}
        return response


