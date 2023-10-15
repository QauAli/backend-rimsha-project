from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas  import CustomerSchema
from resources.schemas  import CustomerUpdateSchema
from resources.Customerdb import MyDatabase
import hashlib
blp = Blueprint("customer", __name__, description="Operations on customer")

@blp.route("/customer")
class Customer(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     Customer_id = request.args.get("Customer_id")
     if Customer_id is None:
      return self.db.get_customers()
     else:
      customer = self.db.get_customer(Customer_id)
      print(customer)
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
