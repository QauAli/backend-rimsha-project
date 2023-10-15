from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import BillSchema
from resources.schemas import BillUpdateSchema
from resources.Billdb import MyDatabase

blp = Blueprint("Bill", __name__, description="Operations on bill")

@blp.route("/bill")
class Bill(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for reteriving the specific data
    def getall(self):
     Bill_id = request.args.get("Bill_id")
     if Bill_id is None:
      return self.db.get_bills()
     else:
      bill = self.db.get_bill(Bill_id)
      print(bill)
      if bill is None:
          abort(404, message="Record doesn't exist")
      return bill

    def get(self):
        Bill_id = request.args.get("Bill_id")
        if Bill_id is None:
            return self.db.get_bills()
        else:
            bill = self.db.get_bill(Bill_id)
            # print(customer)
            if bill is None:
                abort(404, message="Record doesn't exist")
            return bill

    # post is use for adding the data
    @blp.arguments(BillSchema)
    def post(self,  request_data):
      Bill_id = request_data.get('Bill_id')
      self.db.add_bill(Bill_id, request_data)
      return{'message': "bill added successfully"}, 201




  # put is used for updating the data
    @blp.arguments(BillUpdateSchema)
    def put(self, request_data):
        Bill_id = request_data.get('Bill_id')
        print(f"Received request with ID: {Bill_id}")
        # id = args.get('id')
        if self.db.update_bill(Bill_id, request_data):
            return {'message': "bill updated successfully"}, 201
        abort(404, "bill not found")



# @blp.route('/bill', methods=['DELETE'])

    def delete(self):
        Bill_id = request.args.get('Bill_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_bill(Bill_id):
            return {"message": "bill deleted successfully"}
        abort(404, "bill not found")
