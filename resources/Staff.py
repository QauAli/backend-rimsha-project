from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import StaffSchema
from resources.schemas import StaffUpdateSchema
from resources.Staffdb import MyDatabase

blp = Blueprint("staff", __name__, description="Operations on staff")

@blp.route("/staff")
class Staff(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     id = request.args.get("id")
     if id is None:
      return self.db.get_allstaff()
     else:
      staff = self.db.get_staff(id)
      print(staff)
      if staff is None:
          abort(404, message="Record doesn't exist")
      return staff

    def get(self):
        id = request.args.get("id")
        if id is None:
            return self.db.get_allstaff()
        else:
            staff = self.db.get_staff(id)
            # print(staff)
            if staff is None:
                abort(404, message="Record doesn't exist")
            return staff

    # post is use for adding the data
    @blp.arguments(StaffSchema)
    def post(self,  request_data):
      id = request_data.get('id')
      self.db.add_staff(id, request_data)
      return{'message': "staff member added successfully"}, 201




  # put is used for updating the data
    @blp.arguments(StaffUpdateSchema)
    def put(self, request_data):
        id = request_data.get('id')
        print(f"Received request with ID: {id}")
        # id = args.get('id')
        if self.db.update_staff(id, request_data):
            return {'message': "staff member updated successfully"}, 201
        abort(404, "staff member not found")



# @blp.route('/staff', methods=['DELETE'])

    def delete(self):
        id = request.args.get('id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_staff(id):
            return {"message": "staff member deleted successfully"}
        abort(404, "staff member not found")
